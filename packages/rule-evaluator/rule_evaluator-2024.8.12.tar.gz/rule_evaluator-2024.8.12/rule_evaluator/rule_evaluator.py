import re
from collections import OrderedDict

def preprocess_rule(rule: str) -> str:
    """
    Preprocess the rule to convert space-separated tokens inside nested parentheses
    into 'AND' expressions.

    Args:
        rule (str): The rule to preprocess.

    Returns:
        str: The preprocessed rule.
    """
    # Use a stack to handle nested parentheses
    stack = []
    current = ""
    
    for char in rule:
        if char == '(':
            # Push the current string onto the stack and start a new string
            stack.append(current)
            current = ""
        elif char == ')':
            # Replace spaces within the current string with " and "
            current = current.replace(' ', ' and ')
            # Pop the last string from the stack and append the modified current string
            current = stack.pop() + f"({current})"
        else:
            current += char
    
    return current

def rule_splitter(rule: str, split_characters: set = {"+","-",",","(",")", " "}) -> set:
    """
    Split rule by characters.

    Args:
        rule (str): Boolean logical string.
        split_characters (list): List of characters to split in rule.

    Returns:
        set: Unique tokens in a rule.
    """
    if not isinstance(rule, str):
        raise ValueError("rule must be a string type")
    rule_decomposed = str(rule)
    if split_characters:
        for character in split_characters:
            character = character.strip()
            if character:
                rule_decomposed = rule_decomposed.replace(character, " ")
    unique_tokens = set(filter(bool, rule_decomposed.split()))
    return unique_tokens

def evaluate_rule(rule: str, tokens: set, replace={"+": " and ", ",": " or "}) -> bool:
    """
    Evaluate a string of boolean logicals.

    Args:
        rule (str): Boolean logical string.
        tokens (set): List of tokens in rule.
        replace (dict, optional): Replace boolean characters. Defaults to {"+":" and ", "," : " or "}.

    Returns:
        bool: Evaluated rule.
    """
    # Preprocess the rule to handle nested rules with spaces
    rule = preprocess_rule(rule)

    # Handle optional tokens prefixed by '-'
    rule = re.sub(r'-\w+', '', rule)

    # Replace characters for standard logical formatting
    for character_before, character_after in replace.items():
        rule = rule.replace(character_before, character_after)

    # Create a dictionary with the presence of each symbol in the tokens
    token_to_bool = {sym: (sym in tokens) for sym in re.findall(r'\w+', rule)}

    # Parse and evaluate the rule using a recursive descent parser
    def parse_expression(expression: str) -> bool:
        expression = expression.strip()
        
        # Handle nested expressions
        if expression.startswith('(') and expression.endswith(')'):
            return parse_expression(expression[1:-1])
        
        # Evaluate 'OR' conditions
        if ' or ' in expression:
            parts = expression.split(' or ')
            return any(parse_expression(part) for part in parts)
        
        # Evaluate 'AND' conditions
        elif ' and ' in expression:
            parts = expression.split(' and ')
            return all(parse_expression(part) for part in parts)
        
        # Evaluate individual token presence
        else:
            return token_to_bool.get(expression.strip(), False)

    return parse_expression(rule)

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


def evaluate_definition(definition: str, tokens: set, replace={"+": " and ", ",": " or "}) -> dict:
    """
    Evaluate a complex definition string involving multiple rules.

    Args:
        definition (str): Complex boolean logical string with multiple rules.
        tokens (set): Set of tokens to check against the rules.
        replace (dict, optional): Replace boolean characters. Defaults to {"+":" and ", "," : " or "}.

    Returns:
        dict: Dictionary with each rule and its evaluated result.
    """
    # Extract individual rules from the definition
    rules = find_rules(definition)
    
    # Evaluate each rule
    rule_results = OrderedDict()
    for rule in rules:
        try:
            cleaned_rule = rule[1:-1] if rule.startswith('(') and rule.endswith(')') else rule  # Remove outer parentheses if they exist
            result = evaluate_rule(cleaned_rule, tokens, replace)
        except SyntaxError:
            # Handle syntax errors from eval() due to incorrect formatting
            result = False
        rule_results[rule] = result
    
    return rule_results


class Rule(object):
    def __init__(
        self,
        rule:str,
        name:str=None,
        replace:dict={"+": " and ", ",": " or "},
        split_characters: set = {"+","-",",","(",")", " "}
    ):
        self.rule = rule
        self.replace = {} if replace is None else replace
        self.name = name
        self.tokens = rule_splitter(rule, split_characters)

    def get_tokens(self):
        return self.tokens
    
    def evaluate(self, tokens:set) -> bool:
        return evaluate_rule(self.rule, tokens, self.replace)

    def __repr__(self):
        return f"Rule[{self.name}]({self.rule})" if self.name else f"Rule({self.rule})"
    
class Definition(object):
    def __init__(
        self,
        definition:str,
        name:str=None,
        replace:dict={"+": " and ", ",": " or "},
        split_characters: set = {"+","-",",","(",")", " "}
    ):
        self.definition = definition
        self.replace = {} if replace is None else replace
        self.split_characters = split_characters
        self.name = name
        self.tokens = rule_splitter(definition, split_characters) #set.union(*map(lambda rule: rule_splitter(rule, self.replace.keys()), find_rules(definition)))
        self.rules = list(map(lambda rule: Rule(rule=rule, replace=replace), find_rules(definition)))
        
    def evaluate(self, tokens:set, score:bool=False) -> dict:
        rule_to_bool = evaluate_definition(self.definition, tokens=tokens, replace=self.replace)
        if score:
            values = rule_to_bool.values()
            return sum(values)/len(values)
        else:
            return rule_to_bool
            
    def get_tokens(self):
        return self.tokens

    def get_rules(self):
        return self.rules

    def __repr__(self):
        return f"Definition[{self.name}]({self.definition})" if self.name else f"Definition({self.definition})"
