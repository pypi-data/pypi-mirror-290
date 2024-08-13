from cleora_saas_api.api.api import get_run_info
from cleora_saas_api.api.dto_keys import (
    INPUT_HASH,
    INPUT_NAME,
    INPUT_PATH,
    MEMORY,
    RUN_ID,
)
from cleora_saas_api.input_details.input_file_details import InputFileDetails
from cleora_saas_api.token.token_managment import get_id_token


def generete_input_from_run_by_id(run_id):
    id_token = get_id_token()
    run_info = get_run_info({RUN_ID: run_id}, id_token)
    return InputFileDetails(
        input_name=run_info[INPUT_NAME],
        input_hash=run_info[INPUT_HASH],
        input_path=run_info[INPUT_PATH],
        memory=run_info[MEMORY],
    )
