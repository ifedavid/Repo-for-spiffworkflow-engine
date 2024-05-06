import subprocess
import json



def add_and_commit_changes(global_var: dict[str, str]):
    files = global_var["files"]
    add_files = subprocess.run(f"git add {files}")
    print(add_files)
    if add_files.returncode == 0:
        COMMIT_MESSAGE = "committing-update-from-workflow-engine"
        subprocess.run(f"git commit -m {COMMIT_MESSAGE}")
        return json.dumps(True)
    return json.dumps(False)


def update_branch(files: str):
    branch = subprocess.run("git branch --show-current")
    print(branch.stdout)
    return json.dumps(True)

def push_updates(files: str):
    return json.dumps(True)

def create_pr(files: str):
    return json.dumps(True)

def create_issue(files: str):
    return json.dumps(True)

def create_gist(files: str):
    return json.dumps(True)
