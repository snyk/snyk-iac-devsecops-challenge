import argparse
import os
import sys
import subprocess
import json

args_parser = argparse.ArgumentParser()
args_parser.add_argument('Path',
    metavar='path',
    type=str,
    help='root directory to search for modules')
args = args_parser.parse_args()

def find_terraform_modules(input_path):
    terraform_modules = []
    for root, dirs, files in os.walk(input_path):
        if any([True for f in files if f.endswith(".tf")]):
            terraform_modules.append(root)
            continue
    return terraform_modules

def exec_terraform_validate(cwd):
    subprocess.run(["terraform", "init"], cwd=cwd, capture_output=True)
    proc = subprocess.Popen(["terraform", "validate", "-json"], cwd=cwd, stdout=subprocess.PIPE)
    streamout = proc.communicate()[0]
    if proc.returncode != 0:
        sys.exit("[-] failed to run terraform validate on {}. {}".format(cwd, streamout))
    return json.loads(streamout.decode().replace("\n", ""))

def exec_terraform_plan(cwd):
    proc = subprocess.Popen(["terraform", "plan", "-json"], cwd=cwd, stdout=subprocess.PIPE)
    result = []
    while True:
        log_line = proc.stdout.readline()
        if not log_line:
            break
        result.append(json.loads(log_line))
    proc.communicate()
    if proc.returncode != 0:
        sys.exit("[-] failed to run terraform plan on {}".format(cwd))
    return result

def report(data):
    for module_path in data:
        print("Module: {}".format(module_path))
        for result_type, result_data in data[module_path].items():
            print("{}: {}".format(result_type, result_data))

def main():
    input_path = args.Path
    terraform_modules = find_terraform_modules(input_path)
    results = {}
    for terraform_module in terraform_modules:
        results[terraform_module] = {}
        results[terraform_module]["terraform_validate"] = exec_terraform_validate(terraform_module)
        results[terraform_module]["terraform_plan"] = exec_terraform_plan(terraform_module)
    report(results)
                

if __name__ == "__main__":
    main()
