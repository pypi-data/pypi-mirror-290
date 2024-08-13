import os
from pathlib import Path
from cleora_saas_api.config import GIGA_FACTOR
from cleora_saas_api.file_hash import get_file_hash
from cleora_saas_api.find_input_in_existing_runs import find_input_in_existing_runs

from cleora_saas_api.api.api import get_runs
from cleora_saas_api.input_details.input_file_details import InputFileDetails
from cleora_saas_api.token.token_managment import get_id_token


def generate_input_from_local(input_path: str):
    id_token = get_id_token()
    is_input_local = os.path.exists(input_path)
    if is_input_local:
        runs = get_runs(id_token)
        input_file_details = find_input_in_existing_runs(input_path, runs)
        if input_file_details == None:
            input_file_details = InputFileDetails(
                input_name=Path(input_path).name,
                input_path=None,
                memory=str(os.path.getsize(input_path) / GIGA_FACTOR),
                input_hash=get_file_hash(input_path),
            )
            input_file_details.set_is_local_file(True)
        return input_file_details
    else:
        raise Exception("Provided input_path do not exist")
