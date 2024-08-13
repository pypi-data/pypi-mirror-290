from cleora_saas_api.api.api import get_runs
from cleora_saas_api.find_input_in_existing_runs import (
    find_input_in_existing_runs_by_run_name,
)
from cleora_saas_api.token.token_managment import get_id_token


def generate_input_from_input_name(input_name: str):
    id_token = get_id_token()
    runs = get_runs(id_token)
    return find_input_in_existing_runs_by_run_name(input_name, runs)
