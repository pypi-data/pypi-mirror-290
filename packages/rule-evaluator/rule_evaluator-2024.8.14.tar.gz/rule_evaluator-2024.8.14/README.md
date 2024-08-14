# Rule Evaluator
Lightweight Python-based nested rule evaluator. 

## Installation:

```
pip install rule_evaluator
```

## Usage: 

```python
import rule_evaluator as rl
```

### Rule evaluation:

```python
import rule_evaluator as rl
from collections import OrderedDict

# Define the rules
rules = [
    'R00351', # False
    'R01325+R01900,R01324', # True
    'R01899+R00268,R00267,R00709', # True
    'R00621+R03316,R01700', # True
    'R02570', # True
    'R07618', # True
    'R01197', # True
    'R00405,R00432,R00727,R10343', # False
    'R02164', # True
    'R01082', # True
    'R00342,R00361'# True
]

# List of elements to query
elements = {
    # "R00351", 
    # "R01325",
    # 'R01900',
    "R01324",
    'R00267',
    'R00342',
    'R00361',
    'R00621',
    'R03316',
    'R00709',
    # 'R00405',
    # "R01700",
    # 'R00727',
    # 'R00432',
    # 'R10343'
    'R01082',
    'R01197',
    'R01899',
    'R00268',
    'R02164',
    'R02570',
    'R07618',
}

rule_to_bool = OrderedDict()
for rule in rules:
    rule_to_bool[rule] = rl.Rule(rule).evaluate(elements)
rule_to_bool
# OrderedDict([('R00351', False),
#              ('R01325+R01900,R01324', True),
#              ('R01899+R00268,R00267,R00709', True),
#              ('R00621+R03316,R01700', True),
#              ('R02570', True),
#              ('R07618', True),
#              ('R01197', True),
#              ('R00405,R00432,R00727,R10343', False),
#              ('R02164', True),
#              ('R01082', True),
#              ('R00342,R00361', True)])

```

### Definition evaluation:

```python
import rule_evaluator as rl

# Define the nested rules
name="M00357"
definition = '((K00925 K00625),K01895) (K00193+K00197+K00194) (K00577+K00578+K00579+K00580+K00581-K00582-K00583+K00584) (K00399+K00401+K00402) (K22480+K22481+K22482,K03388+K03389+K03390,K08264+K08265,K03388+K03389+K03390+K14127+(K14126+K14128,K22516+K00125))'

# List of elements to check against
elements = {
    'K00925',
    # 'K00625',
    # 'K01895',
    'K00193',
    'K00197',
    'K00194',
    'K00577',
    'K00578',
    'K00579',
    'K00580',
    'K00581',
    'K00582',
    'K00584',
    'K00399',
    'K00401',
    'K00402',
    # 'K22480',
    # 'K22481',
    # 'K22482',
    # 'K03388',
    # 'K03389',
    # 'K03390',
    # 'K08264',
    # 'K08265',
    # 'K14127',
    # 'K14126',
    # 'K14128',
    # 'K22516',
    # 'K00125'
}

# Define
d = rl.Definition(definition, name=name, element_type="ko")

# View Defintion
d
# ========================================
# Definition(name:M00357, element_type:ko)
# ========================================
# Properties:
#     - number_of_elements: 30
#     - number_of_rules: 5
# Rules:
#     - 0: ((K00925 K00625),K01895)
#     - 1: (K00193+K00197+K00194)
#     - 2: (K00577+K00578+K00579+K00580+K00581-K00582-K00583+K00584)
#     - 3: (K00399+K00401+K00402)
#     - 4: (K22480+K22481+K22482,K03388+K03389+K03390,K08264+K08265,K03388+K03389+K03390+K14127+(K14126+K14128,K22516+K00125))

# View Rule
d.rules[2]
# =========================================================
# Rule(name:2, element_type:ko)
# =========================================================
# (K00577+K00578+K00579+K00580+K00581-K00582-K00583+K00584)
# _________________________________________________________
# Properties:
#     - number_of_elements: 8


# Evaluate
d.evaluate(elements)
# OrderedDict([('((K00925 K00625),K01895)', False),
#              ('(K00193+K00197+K00194)', True),
#              ('(K00577+K00578+K00579+K00580+K00581-K00582-K00583+K00584)',
#               True),
#              ('(K00399+K00401+K00402)', True),
#              ('(K22480+K22481+K22482,K03388+K03389+K03390,K08264+K08265,K03388+K03389+K03390+K14127+(K14126+K14128,K22516+K00125))',
#               False)])

# Score
d.evaluate(elements, score=True)
# 0.6 
```

# Acknowledgements:
This package would not be possible without the grammar parsing help of [@flakes](https://stackoverflow.com/users/3280538/flakes).
