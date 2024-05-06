from SpiffWorkflow.bpmn.script_engine import TaskDataEnvironment
from business_logic import add_and_commit_changes, update_branch, push_updates, create_gist, create_issue, create_pr
from enum import StrEnum


class Process(StrEnum):
    ADD_AND_COMMIT_CHANGES = "process_add_and_commit_changes"
    UPDATE_BRANCH = "process_update_branch"
    PUSH_UPDATES = "process_push_updates"
    CREATE_PR = "process_create_PR"
    CREATE_GIST = "process_create_gist"
    CREATE_ISSUE = "process_create_issue"


class ServiceTaskEnvironment(TaskDataEnvironment):
    def evaluate(self, expression, context, external_context=None):
        self.globals.update({"value": context})
        return context

    def call_service(self, operation_name, operation_params, task_data):
        process_function_map = {
            Process.ADD_AND_COMMIT_CHANGES: add_and_commit_changes,
            Process.UPDATE_BRANCH: update_branch,
            Process.PUSH_UPDATES: push_updates,
            Process.CREATE_PR: create_pr,
            Process.CREATE_GIST: create_gist,
            Process.CREATE_ISSUE: create_issue
        }
        try:
            return process_function_map[operation_name](self.globals)
        except(Exception):
            print("something went wrong")
