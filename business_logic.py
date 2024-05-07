import subprocess
import json
import requests

BASE_GITHUB_URL = "https://api.github.com"
GITHUB_TOKEN = "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"


def add_and_commit_changes(global_var: dict[str, str]):
    files = global_var["files"]
    add_files = subprocess.run(f"git add {files}")
    if add_files.returncode == 0:
        COMMIT_MESSAGE = "committing-update-from-workflow-engine"
        subprocess.run(f"git commit -m {COMMIT_MESSAGE}")
        return json.dumps({"success": "Added and commited changes sucessfully"})
    return json.dumps({"error": "something wrong happened"})


def update_branch(global_var: dict[str, str]):
    current_branch = subprocess.Popen(
        "git branch --show-current", stdout=subprocess.PIPE
    )
    current_branch_name = current_branch.stdout.read().decode("utf-8")
    current_branch_name = current_branch_name.strip()
    if current_branch_name == "main":
        new_branch_name = get_branch_name()
        subprocess.run(f"git checkout -b {new_branch_name}")
        return json.dumps(
            {
                "success": "Updated branch sucessfully",
                "new_branch_name": new_branch_name,
            }
        )
    return json.dumps({"passed": "Skipping branch update", "new_branch_name": current_branch_name})


def push_updates(global_var: dict[str, str]):
    branch_name = global_var["new_branch_name"]
    subprocess.run(f"git push --set-upstream origin {branch_name}")
    success_respone = f"Pushed remote branch {branch_name} sucessfully"
    return json.dumps({"success": success_respone})


def create_pr(global_var: dict[str, str]):
    pr_url = BASE_GITHUB_URL + "/repos/ifedavid/repo-for-spiffworkflow-engine/pulls"
    branch_name = global_var.get("new_branch_name")
    pr_title = f"Spiff workflow automatd PR for branch - {branch_name}"
    pr_body = "Playing around with Spiffworkflow to automate PR creation. This is one of the automated PRs"
    head = branch_name
    base = "main"
    response = requests.post(
        url=pr_url,
        data=json.dumps(
            {"title": pr_title, "body": pr_body, "head": head, "base": base}
        ),
        headers={
            "Authorization": "token " + GITHUB_TOKEN,
            "X-GitHub-Api-Version": "2022-11-28",
            "accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
    )

    if response.status_code == 201:
        created_pr_url = response.json().get("html_url")
        return json.dumps(
            {"success": "success_respone", "created_pr_url": created_pr_url}
        )

    error_message = f"{response.text} {response.status_code}"
    return json.dumps(
        {"error": "something went wrong" + error_message, "created_pr_url": None}
    )


def create_gist(global_var: dict[str, str]):
    pr_url = BASE_GITHUB_URL + "/gists"
    branch_name = global_var.get("new_branch_name")
    created_pr_url = global_var.get("created_pr_url")
    created_issue_url = global_var.get("created_issue_url")
    gist_description = f"Spiff workflow automatd gist for branch - {branch_name}"
    file_name = f"{branch_name}.md"
    file_content = f"automated gist file to keep track of PR - {created_pr_url} and Issue - {created_issue_url}"
    response = requests.post(
        url=pr_url,
        data=json.dumps(
            {"description": gist_description, "files": {file_name: {"content": file_content}}, "public": True}
        ),
        headers={
            "Authorization": "token " + GITHUB_TOKEN,
            "X-GitHub-Api-Version": "2022-11-28",
            "accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
    )

    if response.status_code == 201:
        created_gist_url = response.json().get("html_url")
        return json.dumps(
            {"success": "success_respone", "created_gist_url": created_gist_url}
        )

    error_message = f"{response.text} {response.status_code}"
    return json.dumps(
        {"error": "something went wrong" + error_message, "created_gist_url": None}
    )


def create_issue(global_var: dict[str, str]):
    pr_url = BASE_GITHUB_URL + "/repos/ifedavid/repo-for-spiffworkflow-engine/issues"
    created_pr_url = global_var.get("created_pr_url")
    issue_title = f"Spiff workflow automatd issue."
    issue_body = f"Playing around with Spiffworkflow to automate Issue creation. This is one of the automated Issues, automatd issue for PR - {created_pr_url}"
    response = requests.post(
        url=pr_url,
        data=json.dumps({"title": issue_title, "body": issue_body}),
        headers={
            "Authorization": "token " + GITHUB_TOKEN,
            "X-GitHub-Api-Version": "2022-11-28",
            "accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
    )

    if response.status_code == 201:
        created_issue_url = response.json().get("html_url")
        return json.dumps(
            {"success": "success_respone", "created_issue_url": created_issue_url}
        )

    error_message = f"{response.text} {response.status_code}"
    return json.dumps(
        {"error": "something went wrong" + error_message, "created_issue_url": None}
    )


def get_branch_name():
    api_url = "https://api.api-ninjas.com/v1/randomuser"
    response = requests.get(
        api_url, headers={"X-Api-Key": "7KX6ycTlMvCgvdQ5PyaMmQ==5cLtxXBQIj4z0rDG"}
    )
    if response.status_code == requests.codes.ok:
        return response.json()["name"].replace(" ", "-")
    else:
        print("Error:", response.status_code, response.text)
