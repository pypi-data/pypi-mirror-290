import subprocess, sys, json
from testrail_api import TestRailAPI

def is_duplicate_test_case_ids(list):
    if len(list) != len(set(list)):
        return True
    else:
        return False
    
def upload_to_testrail(project_id, milestone_id,suite_id, testrun_name, case_ids, host, username, password):

    api = TestRailAPI(host, username, password)

    print("\n============= START TO CREATE TEST RUN ==============\n")

    run = api.runs.add_run(
        project_id=project_id,
        milestone_id=milestone_id,
        suite_id=suite_id,
        name=testrun_name,
        include_all= False,
        case_ids= case_ids
    )
    run_id = str(run['id'])
    print("TEST RUN : https://amarthaqa.testrail.io/index.php?/runs/view/" + run_id)
    print("\n============== SUCCESS CREATE TEST RUN ==============\n")
    print("=====================================================")
    print("=====================================================")
    print("\n========== START UPLOAD RESULT TO TESTRAIL ==========\n")
    subprocess.run('trcli -n -h https://amarthaqa.testrail.io --project "Amartha Automation Execution" --project-id '+project_id+' --username qa.eng@amartha.com --password Amartha2021 parse_junit --case-matcher "property" --title "'+testrun_name+'" --suite-id '+suite_id+' --milestone-id '+milestone_id+' --run-id '+run_id+' -f junit_report.xml', shell=True, check=True, timeout=240)
    print("=====================================================")
    print("=====================================================")

def get_running_test_case_ids():
    file = open("test_id_temp.txt", "r")

    case_ids = file.read()
    chars = ["'", ' ', '[', ']']
    for i in chars:
        case_ids = case_ids.replace(i, '')
    case_ids = case_ids.split(',')

    file.close()
    return case_ids