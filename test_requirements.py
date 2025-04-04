import sys
import subprocess
import os
import json

def run_deptry(reqs, rule_ignores, path, extra_args=""):
    """Run a dependency check with deptry. Return a list of error messages"""

    errors = []
    try:
        result = subprocess.run(
            f"deptry -o deptry.json --no-ansi --known-first-party mindsdb --requirements-txt \"{reqs}\" {extra_args} {path}",
            shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
        )
        if result.returncode != 0 and not os.path.exists("deptry.json"):
            # There was some issue with running deptry
            errors.append(f"Error running deptry: {result.stderr.decode('utf-8')}")

        with open("deptry.json", "r") as f:
            deptry_results = json.loads(f.read())
        for r in deptry_results:
            if 'type_infer' in r['error']['message']:
                errors.append(f"{r['location']['line']}:{r['location']['column']}: {r['error']['code']} {r['error']['message']}")
    finally:
        if os.path.exists("deptry.json"):
            os.remove("deptry.json")
    return errors

# Run against the main requirements file
errors = run_deptry(
    "requirements/requirements.txt",
    "",
    ".",
)

print("--- Checking that requirements match imports ---")
print("- requirements/requirements.txt")
for error in errors:
    print(f"    {error}")

# Check if type_infer is used in the handlers
print("\n--- Checking handlers that use type_infer ---")
handlers_using_type_infer = []
for root, dirs, files in os.walk("mindsdb/integrations/handlers"):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                content = f.read()
                if 'from type_infer' in content or 'import type_infer' in content:
                    handlers_using_type_infer.append(file_path)

for handler in handlers_using_type_infer:
    print(f"    {handler}")

# Check if type_infer is included in handler requirements
print("\n--- Checking if type_infer is in handler requirements ---")
for handler_path in handlers_using_type_infer:
    handler_dir = os.path.dirname(handler_path)
    req_file = os.path.join(handler_dir, "requirements.txt")
    if os.path.exists(req_file):
        with open(req_file, 'r') as f:
            content = f.read()
            if 'type_infer' in content:
                print(f"    {req_file}: type_infer is included")
            else:
                print(f"    {req_file}: type_infer is NOT included")