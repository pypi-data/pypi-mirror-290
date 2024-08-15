import re
from collections import OrderedDict
from typing import List, Protocol
from dataclasses import dataclass
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

# Format header for printing
def format_header(text, line_character="=", n=None):
    if n is None:
        n = len(text)
    line = n*line_character
    return "{}\n{}\n{}".format(line, text, line)

# Split rules into
def split_rule(rule: str, split_characters: set = {"+","-",",","(",")", " "}) -> set:
    """
    Split rule by elements.

    Args:
        rule (str): Boolean logical string.
        split_characters (list): List of characters to split in rule.

    Returns:
        set: Unique elements in a rule.
    """
    if not isinstance(rule, str):
        raise ValueError("rule must be a string type")
    rule_decomposed = str(rule)
    if split_characters:
        for character in split_characters:
            character = character.strip()
            if character:
                rule_decomposed = rule_decomposed.replace(character, " ")
    unique_elements = set(filter(bool, rule_decomposed.split()))
    return unique_elements

# Find rules in a definition
def find_rules(definition: str) -> list:
    """
    Find and extract rules from the definition string.

    Args:
        definition (str): Complex boolean logical string with multiple rules.

    Returns:
        list: List of extracted rules as strings.
    """
    rules = []
    stack = []
    current_rule = ""
    outside_rule = ""

    for char in definition:
        if char == '(':
            if stack:
                current_rule += char
            if outside_rule.strip():
                rules.append(outside_rule.strip())
                outside_rule = ""
            stack.append(char)
        elif char == ')':
            stack.pop()
            if stack:
                current_rule += char
            else:
                current_rule = f"({current_rule.strip()})"
                rules.append(current_rule)
                current_rule = ""
        else:
            if stack:
                current_rule += char
            else:
                outside_rule += char

    # Add any remaining outside_rule at the end of the loop
    if outside_rule.strip():
        rules.append(outside_rule.strip())

    return rules



# ________________________________________________________________________

# ==============
# Grammar Parser
# ==============
# The following code and descriptions is sourced (with light modifications) from @flakes (https://stackoverflow.com/users/3280538/flakes): 
#     https://stackoverflow.com/a/78837254/678572


# Defining the grammar
# -------------------
# Given the rules, you've defined a few operators with different precedence.

# Break all values by the or operator ","
# Break all top level items by the rules " "
# Break all values by the and operator "+" or ignore operator "-"
# "+" and "-" have the same precedence
# Values may be defined in braces "(...)"
# These are to be recursively parsed by referencing the root definition.
# Given these rules, here's how you can define a grammar.
DEFAULT_RULE_GRAMMAR="""
    maybe_or = (maybe_rule or+) / maybe_rule
    or = "," maybe_rule
    
    maybe_rule = (maybe_and rule+) / maybe_and
    rule = " " maybe_and
    
    maybe_and = (expression and+) / expression
    and = and_op expression
    and_op = "+" / "-"
    
    expression = brace_expression / variable
    brace_expression = "(" maybe_or ")"
    
    variable = ~r"[A-Z0-9]+"
"""
grammar = Grammar(DEFAULT_RULE_GRAMMAR)


# Defining containers
# -------------------
# Now that we have a grammar, we can construct containers to represent its hierarchy. We'll want to be able to test against 
# the items set by evaluating each container against its children.
# At this point we can consider which of the operators need to be defined by separate containers. 
# The and-operation "+" and rules operator " " have the same boolean evaluation, so we can combine them to a single And class. 
# Other containers would be Or, Ignored and Var to represent the bool var codename.
# We'll also benefit from a str repr to see whats going on in the case of errors, which we can use to dump out a normalized version of the expression.

class Matcher(Protocol):
    def matches(self, variables: List[str]) -> bool:
        pass

@dataclass
class Var:
    value: str

    def __str__(self):
        return self.value

    def matches(self, variables: List[str]) -> bool:
        return self.value in variables

@dataclass
class Ignored:
    value: Matcher

    def __str__(self):
        return f"{self.value}?"

    def matches(self, variables: List[str]) -> bool:
        return True

@dataclass
class And:
    values: List[Matcher]

    def __str__(self):
        return "(" + "+".join(map(str, self.values))  + ")"

    def matches(self, variables: List[str]) -> bool:
        return all(v.matches(variables) for v in self.values)

@dataclass
class Or:
    values: List[Matcher]

    def __str__(self):
        return "(" + ",".join(map(str, self.values)) + ")"

    def matches(self, variables: List[str]) -> bool:
        return any(v.matches(variables) for v in self.values)

# Parsing the grammar
# -------------------
# With a grammar and a set of containers we can now begin to unpack the statement. 
# We can use the NodeVistor class from parsimonious for this. Each definition in the grammar 
# can be given its own handler method to use while unpacking values.

class Visitor(NodeVisitor):
    def visit_maybe_rule(self, node, visited_children):
        # If there are multiple rules, combine them.

        children, *_ = visited_children
        if isinstance(children, list):
            return And([children[0], *children[1]])
        return children

    def visit_rule(self, node, visited_children):
        # Strip out the " " rule operator child element

        return visited_children[1]

    def visit_maybe_or(self, node, visited_children):
        # If there are multiple or values, combine them.

        children, *_ = visited_children
        if isinstance(children, list):
            return Or([children[0], *children[1]])
        return children

    def visit_or(self, node, visited_children):
        # Strip out the "," or operator child element

        return visited_children[1]

    def visit_maybe_and(self, node, visited_children):
        # If there are multiple and values, combine them.

        children, *_ = visited_children
        if isinstance(children, list):
            return And([children[0], *children[1]])
        return children

    def visit_and(self, node, visited_children):
        # Strip out the operator child element, and
        # handle the case where we ignore values.

        if visited_children[0] == "-":
            return Ignored(visited_children[1])
        return visited_children[1]

    def visit_and_op(self, node, visited_children):
        # get the text of the operator.

        return node.text

    def visit_expression(self, node, visited_children):
        # expressions only have one item

        return visited_children[0]

    def visit_brace_expression(self, node, visited_children):
        # Strip out the "(" opening and ")" closing braces

        return visited_children[1]

    def visit_variable(self, node, visited_children):
        # Parse the variable name

        return Var(node.text)

    def generic_visit(self, node, visited_children):
        # Catchall response.

        return visited_children or node
    
# Usage:
# grammar = Grammar(DEFAULT_RULE_GRAMMAR)
# for rule in definitions:
#     tree = grammar.parse(rule)
#     val = Visitor().visit(tree)
#     print(f"Test: {rule}")
#     print(f"Parsed as: {val}")
#     print(f"Result: {val.matches(items)}")
#     print()
# ________________________________________________________________________

# Classes
class Rule(object):
    def __init__(
        self,
        rule:str,
        name:str=None,
        element_type:str=None,
        split_characters: set = {"+","-",",","(",")", " "},
        rule_grammar:str=DEFAULT_RULE_GRAMMAR,
    ):
        if not isinstance(rule, str):
            raise ValueError("rule must be string")
        self.rule = str(rule)
        self.name = name
        self.element_type = element_type
        self.elements = split_rule(rule, split_characters)
        self.number_of_elements = len(self.elements)
        self.grammar = Grammar(DEFAULT_RULE_GRAMMAR)
        self.tree = self.grammar.parse(rule)
        self.tree_walker = Visitor().visit(self.tree)

    def get_elements(self):
        return self.elements
    
    def evaluate(self, elements:set) -> bool:
        return self.tree_walker.matches(elements)

    def __repr__(self):
        name_text = "{}(name:{}, element_type:{})".format(self.__class__.__name__, self.name, self.element_type)
        rule_text = "{}".format(self.rule)
        n = max(len(name_text), len(rule_text))
        pad = 4
        fields = [
            format_header(name_text,line_character="=", n=n),
            *format_header(rule_text, line_character="_", n=n).split("\n")[1:],
            "Properties:",
            pad*" " + "- number_of_elements: {}".format(self.number_of_elements),
        ]
        return "\n".join(fields)
    
class Definition(object):
    def __init__(
        self,
        definition:str,
        name:str=None,
        element_type:str=None,
        split_characters: set = {"+","-",",","(",")", " "},
        rule_grammar:str=DEFAULT_RULE_GRAMMAR,
    ):
        if not isinstance(definition, str):
            raise ValueError("definition must be string")
        self.definition = str(definition)
        self.split_characters = split_characters
        self.name = name
        self.element_type = element_type
        self.elements = split_rule(definition, split_characters) #set.union(*map(lambda rule: split_rule(rule, self.replace.keys()), find_rules(definition)))
        self.number_of_elements = len(self.elements)
        self.rules = list()
        for i,rule in enumerate(find_rules(definition)):
            rule = Rule(rule=rule, name=i, split_characters=split_characters, rule_grammar=rule_grammar, element_type=self.element_type)
            self.rules.append(rule)
        self.number_of_rules = len(self.rules)
        
    def evaluate(self, elements:set, score:bool=False) -> dict:
        rule_to_bool = dict() #evaluate_definition(self.definition, elements=elements, replace=self.replace)
        for rule in self.rules:
            rule_to_bool[rule.rule] = rule.evaluate(elements)
        if score:
            values = rule_to_bool.values()
            return sum(values)/len(values)
        else:
            return rule_to_bool
            
    def get_elements(self):
        return self.elements

    def get_rules(self):
        return self.rules

    def __repr__(self):
        name_text = "{}(name:{}, element_type:{})".format(self.__class__.__name__, self.name, self.element_type)
        n = len(name_text)
        pad = 4
        fields = [
            format_header(name_text,line_character="=", n=n),        
            "Properties:",
            pad*" " + "- number_of_elements: {}".format(self.number_of_elements),
            pad*" " + "- number_of_rules: {}".format(self.number_of_rules),
            "Rules:",
            ]
        for rule in self.rules:
            rule_text = pad*" " + "- {}: {}".format(rule.name, rule.rule)
            fields.append(rule_text)
        return "\n".join(fields)
    
# Chemistry
def split_reaction_equation(
    equation:str, 
    stoichiometric_coefficient:bool=True, 
    sep_left_right:str=" <=> ", 
    compound_splitter:str=" + ",
    ) -> tuple:
    """Split reaction equations with or without stoichiometric coefficients

    Args:
        equation (str): Reaction equation
            With stoichiometric coefficients:
                3 C00083 + 5 C02557 + 7 C00005 + 7 C00080 <=> C15685 + 8 C00010 + 8 C00011 + 4 C00001 + 7 C00006)
            or without stoichiometric coefficients:
                C00002 + 5 C00065 <=> C00008 + C01005
        stoichiometric_coefficient (bool, optional): Output includes stoichiometric coefficients. Defaults to True.
        sep_left_right (str, optional): Separator between left and right reactions. Defaults to " <=> ".
        compound_splitter (str, optional): Split compounds in each half-reaction. Defaults to " + ".
        
    Returns:
        Tuple (left_reactions, right_reactions)
    """
    def _format_compounds(half_reaction_equation:str, compound_splitter):
        compounds = list()
        for cpd in half_reaction_equation.split(compound_splitter):
            cpd = cpd.strip()
            if " " in cpd:
                if not cpd[0].isdigit():
                    raise ValueError(
                        f"Could not parse '{cpd}'.  \
                        If cpd contains whitespace then it is assumed to start with a digit \
                        (i.e., stoichiometric coefficient)")
                x, id_cpd = cpd.split(" ")
                x = int(x)
            else:
                x = 1
                id_cpd = cpd
            compounds.append((id_cpd,x))
        return compounds
    # Check equation        
    number_of_seperators = equation.count(sep_left_right)
    if number_of_seperators != 1:
        raise IndexError(f"equation should have 1 and only 1 separator: {sep_left_right}")
    left, right = equation.strip().split(sep_left_right)
    # Format left compounds
    left_compounds = _format_compounds(left, compound_splitter=compound_splitter)
    # Format right compounds
    right_compounds = _format_compounds(right, compound_splitter=compound_splitter)

    if not stoichiometric_coefficient:
        left_compounds = list(map(lambda x: x[0], left_compounds))
        right_compounds = list(map(lambda x: x[0], right_compounds))
    
    return left_compounds, right_compounds