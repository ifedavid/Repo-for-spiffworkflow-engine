import subprocess
import json



COMMIT_MESSAGE = "committing-update-from-workflow-engine"

def add_and_commit_changes(files: str):
    print(files)
    add_files = subprocess.run(f"git add {files}")
    if add_files.returncode == 0:
        subprocess.run(f"git commit -m {COMMIT_MESSAGE}")
        return json.dumps(True)
    return json.dumps(False)
