import sys
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from SpiffWorkflow.spiff.parser import SpiffBpmnParser
from SpiffWorkflow.bpmn.script_engine import TaskDataEnvironment

from business_logic import add_and_commit_changes


class ServiceTaskEnvironment(TaskDataEnvironment):
    def evaluate(self, expression, context, external_context=None):
        self.globals.update({"value": context})
        return context

    def call_service(self, operation_name, operation_params, task_data):
        print("here")
        print(self.globals)
        if operation_name == "process_add_and_commit_changes":
            try:
                return add_and_commit_changes(self.globals["files"])
            except(Exception):
                print("something went wrong")
        else:
            raise ValueError('Unknown Service')

def main(files: str):
    parser = SpiffBpmnParser()
    parser.add_bpmn_file('ife_personal_project.bpmn')
    spec = parser.get_spec('Process_ife_personal_project_z157wwm')
    global_var = {"files": files}
    script_env = ServiceTaskEnvironment(global_var)
    workflow = BpmnWorkflow(spec, script_engine=script_env)
    workflow.run_all()



if __name__ == '__main__':
    system_args = sys.argv
    files = " ".join(system_args[0:])
    main(files)

