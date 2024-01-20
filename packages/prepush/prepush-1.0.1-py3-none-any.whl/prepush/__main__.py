import subprocess
import os
import yaml
from pathlib import PurePath

def list_workflow_yaml_files(directory):
    try:
        files = os.listdir(directory)
        yaml_files = []
        for file in files:
            _, extension = os.path.splitext(file)
            if extension.lower() in ['.yaml', '.yml']:
                yaml_files.append(file)
        return yaml_files
    except FileNotFoundError:
        print(f"Directory '{directory}' not found.")
        return []

def run_git_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command {command}: {e.stderr}")
        return None

def cal_changed_files() -> list[str]:
    changed_files = run_git_command(['git', 'diff', '--name-only', 'HEAD', 'HEAD~1'])
    return_files = []
    if changed_files is not None:
        for file in changed_files.split("\n"):
            if file != "":
                return_files.append(file.strip())
    return return_files

def cal_valid_paths(workflow_dir):
    return_dict = dict()
    for file in list_workflow_yaml_files(workflow_dir):
        with open(workflow_dir + file, 'r') as file_stream:
            data = yaml.load(file_stream, Loader=yaml.CLoader)
            all_paths = []
            if True in data:
                if "push" in data[True]:
                    if "paths" in data[True]["push"]:
                        for path in data[True]["push"]["paths"]:
                            all_paths.append(path)
                    elif all_paths == []:
                        all_paths.append('*')
            return_dict[file] = all_paths
    return return_dict

def main():
    git_root_dir = run_git_command(['git', 'rev-parse', '--show-toplevel'])
    if git_root_dir == None:
        print("This is not a git repository")
    else:
        git_root_dir = git_root_dir.strip()

    return_set = set()
    files = cal_changed_files()
    # print(files)
    paths = cal_valid_paths(git_root_dir + '/.github/workflows/')
    for workflow in paths:
        for path in paths[workflow]:
            for file in files:
                if PurePath(file).match(path):
                    return_set.add(workflow)
    if len(return_set) == 0:
        print("no workflows will be triggered")
    for workflow in return_set:
        print(workflow)

if __name__ == "__main__":
    main()
