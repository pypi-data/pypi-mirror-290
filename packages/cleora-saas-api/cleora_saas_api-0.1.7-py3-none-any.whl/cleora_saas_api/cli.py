from cleora_saas_api.api.dto_keys import (
    INFO_LOGS,
    INITIAL_FILE_URL,
    INPUT_PATH,
    OUTPUT_PATH,
    RUN_ID,
    STATUS,
    NAME,
)
from cleora_saas_api.find_string_index import find_string_index
from cleora_saas_api.input_details.create_input_details import create_input_details
from cleora_saas_api.login.login_by_custom_token import login_by_custom_token
from cleora_saas_api.login.login_by_refresh_token import login_by_refresh_token
import fire
import json
import os
from pathlib import Path
import sys
import time

from cleora_saas_api.get_info import print_runs_info
from cleora_saas_api.download import download_file
from cleora_saas_api.token.token_managment import (
    check_login_status_with_showing_message,
    get_id_token,
    remove_credentails_folder,
)
from cleora_saas_api.api.api import (
    get_trigger_body,
    get_run_info,
    get_runs,
    prepare_run,
    trigger_run,
)
from cleora_saas_api.upload import upload_file
from cleora_saas_api.retry_on_failure import retry_on_failure

if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    import collections

    setattr(collections, "MutableMapping", collections.abc.MutableMapping)
    setattr(collections, "Mapping", collections.abc.Mapping)


class CLI:
    def __init__(self):
        pass

    def run(
        self,
        dimension,
        iterations,
        input_path=None,
        input_from_runs_by_run_name=None,
        input_from_runs_by_run_id=None,
        input_from_runs_by_input_name=None,
        run_name=None,
        initialization_path=None,
        output_path="./",
        output_file_name="embeddings.npz",
    ):
        """
        Function to start run.
        Args:
        dimension - size of output embedding array
        iterations - number of interation of cleora repeats
        input - it is or path to local file or name of input file of already existed run
        name - optional argument. It specify name of the run.
        initialization - optional argument. it is path to local file with file with initial embeddings.
        output_path - optional argument. Default is './'. It is a path where file with outputs should be download.
        output_file_name - optional argument. Default is 'embeddings.npz'. It is a name of output file.
        """

        if not check_login_status_with_showing_message():
            return

        print("-- Start --")
        id_token = get_id_token()

        body = {
            "dimension": dimension,
            "numberOfIterations": iterations,
        }

        input_file_details = create_input_details(
            input_path=input_path,
            input_from_runs_by_run_name=input_from_runs_by_run_name,
            input_from_runs_by_run_id=input_from_runs_by_run_id,
            input_from_runs_by_input_name=input_from_runs_by_input_name,
        )

        body = body | input_file_details.get_input_details_dict()

        if run_name is not None:
            body[NAME] = run_name
        if initialization_path is not None:
            initialization_file_name = Path(initialization_path).name
            body["initializationFileName"] = initialization_file_name
        response = prepare_run(body, get_id_token())
        print("-- Config to trigger run prepared --")

        if not response.ok:
            print("ERROR: Something get wrong")
            print(response.text)
            return

        response_parsed = json.loads(response.text)
        external_input_file_path = response_parsed[INPUT_PATH]

        if input_file_details.is_local_file:
            upload_file(input_path, external_input_file_path, get_id_token())

        if initialization_path != None and response_parsed[INITIAL_FILE_URL] != None:
            upload_file(
                initialization_path, response_parsed[INITIAL_FILE_URL], get_id_token()
            )

        body_with_run_id = {RUN_ID: response_parsed[RUN_ID]}

        trigger_body = get_trigger_body(body_with_run_id, get_id_token())

        trigger_response = trigger_run(trigger_body, get_id_token())

        if not trigger_response.ok:
            print("ERROR: Something get wrong")
            print(trigger_response.text)
            return

        print("-- Run started --")

        status = "Pending"
        info_logs = []
        last_printed_log_index = -1
        print("-- Logs: --")

        last_printed_log=""

        while status == "Pending" or status == "Running":
            run_info = retry_on_failure(get_run_info,(body_with_run_id, get_id_token()))
            
            status = run_info[STATUS]
            info_logs = run_info[INFO_LOGS]

            if info_logs == None or len(info_logs)==0 or last_printed_log==info_logs[-1]:
                time.sleep(2)
                continue

            last_printed_log_index = find_string_index(info_logs,last_printed_log)+1       
            [print(log) for log in info_logs[last_printed_log_index:]]
            last_printed_log = info_logs[-1]
            time.sleep(2)

        external_output_path = run_info["outputPath"]

        if status == "Succeeded":
            Path(output_path).mkdir(parents=True, exist_ok=True)
            full_output_path = os.path.join(output_path, output_file_name)
            download_file(external_output_path, full_output_path, get_id_token())

        pass

    def login(self, token=None, custom_token=None):
        """
        Please copy your token from the cleora app (https://app.cleora.ai from user details model) and provide this token as argument to this function to login.
        """
        if token != None:
            login_by_refresh_token(token)
            print("logged in successfully")
            return
        elif custom_token != None:
            login_by_custom_token(custom_token)
        return

    def logout(self):
        """
        Remove credentials.
        """
        remove_credentails_folder()
        print("Logout sucessfully")
        return

    def download(
        self, runId="", run_name="", output_path="./", output_file_name="embeddings.npz"
    ):
        """
        Function to download output file based on runId
        """
        if not check_login_status_with_showing_message():
            return

        if runId == "" and run_name == "":
            print("Please specify runId or name. Both can not be empty")
        id_token = get_id_token()
        if runId != "":
            body_with_run_id = {RUN_ID: runId}
        elif run_name != "":
            runs = get_runs(id_token)
            for run in runs:
                if run[NAME] == run_name:
                    body_with_run_id = {RUN_ID: run[RUN_ID]}
                    break

        if body_with_run_id[RUN_ID] == None:
            print(
                "The run with provided name do not exists.\n Please use 'show_runs' command to check list of runs"
            )
        
        run_info = retry_on_failure(get_run_info,(body_with_run_id, id_token))
        status = run_info[STATUS]
        external_output_path = run_info[OUTPUT_PATH]
        Path(output_path).mkdir(parents=True, exist_ok=True)
        full_output_path = os.path.join(output_path, output_file_name)

        if status == "Succeeded":
            download_file(external_output_path, full_output_path, id_token)
        pass

    def show_runs(self):
        """
        Function to show existing runs
        """
        if not check_login_status_with_showing_message():
            return
        print_runs_info()


def cli():
    try:
        if len(sys.argv) == 2:
            if sys.argv[1] == "--help":
                os.system("cleora-saas-api")
                sys.exit()
        fire.Fire(CLI)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "--help":
            os.system("cleora-saas-api")
            sys.exit()
    fire.Fire(CLI)
