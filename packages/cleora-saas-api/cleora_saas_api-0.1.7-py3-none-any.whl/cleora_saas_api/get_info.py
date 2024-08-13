import json
from cleora_saas_api.api.api import get_runs
from cleora_saas_api.api.dto_keys import INPUT_NAME
from cleora_saas_api.token.token_managment import get_id_token


def print_runs_info():
    id_token = get_id_token()
    runs = get_runs(id_token)
    return [
        print(
            f'runId = {run["runId"]} \n \t name = {run["name"]} | inputName = {run[INPUT_NAME]} \n'
        )
        for run in runs
    ]
