#!/usr/bin/env python3
"""
This script checks if type_infer is in the main requirements.txt and handler requirements.txt files.
"""

import re

def get_requirements_from_file(path):
    """Takes a requirements file path and extracts only the package names from it"""
    pattern = '=|~|>|<| |\n|#|\['
    with open(path, 'r') as main_f:
        reqs = [
            re.split(pattern, line)[0]
            for line in main_f.readlines()
            if re.split(pattern, line)[0]
        ]
    return reqs

# Check main requirements
main_reqs = get_requirements_from_file('requirements/requirements.txt')
print(f"type_infer in main requirements: {'type_infer' in main_reqs}")

# Check handler requirements
handler_files = [
    'mindsdb/integrations/handlers/lightwood_handler/requirements.txt',
    'mindsdb/integrations/handlers/tpot_handler/requirements.txt',
    'mindsdb/integrations/handlers/autogluon_handler/requirements.txt',
    'mindsdb/integrations/handlers/flaml_handler/requirements.txt',
    'mindsdb/integrations/handlers/autosklearn_handler/requirements.txt'
]

for file in handler_files:
    handler_reqs = get_requirements_from_file(file)
    print(f"type_infer in {file}: {'type_infer' in handler_reqs}")