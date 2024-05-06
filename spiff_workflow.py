import sys
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from SpiffWorkflow.spiff.parser import SpiffBpmnParser
from service_environment import ServiceTaskEnvironment
from SpiffWorkflow.camunda.parser import CamundaParser

def main(files: str):
    parser = SpiffBpmnParser()
    parser.add_bpmn_file('github_update_workflow.bpmn')
    spec = parser.get_spec('process_ife_personal_project')
    global_var = {"files": files}
    print(global_var)
    script_env = ServiceTaskEnvironment(global_var)
    workflow = BpmnWorkflow(spec, script_engine=script_env)
    workflow.run_all()



if __name__ == '__main__':
    system_args = sys.argv
    files = " ".join(system_args[1:])
    main(files)

