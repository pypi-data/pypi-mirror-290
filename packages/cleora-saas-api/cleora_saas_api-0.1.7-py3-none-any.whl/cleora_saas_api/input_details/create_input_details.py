from cleora_saas_api.api.dto_keys import RUN_ID
from cleora_saas_api.input_details.generate_input_from_input_name import (
    generate_input_from_input_name,
)
from cleora_saas_api.input_details.generate_input_from_local import (
    generate_input_from_local,
)
from cleora_saas_api.input_details.generate_input_from_run_name import (
    generate_input_from_run_name,
)
from cleora_saas_api.input_details.generete_input_from_run_by_id import (
    generete_input_from_run_by_id,
)
from cleora_saas_api.input_details.input_file_details import InputFileDetails


def create_input_details(
    input_path=None,
    input_from_runs_by_run_id=None,
    input_from_runs_by_run_name=None,
    input_from_runs_by_input_name=None,
) -> InputFileDetails:
    if input_path != None:
        return generate_input_from_local(input_path=input_path)
    if input_from_runs_by_run_id != None:
        return generete_input_from_run_by_id(input_from_runs_by_run_id)
    if input_from_runs_by_run_name != None:
        return generate_input_from_run_name(input_from_runs_by_run_name)
    if input_from_runs_by_input_name != None:
        return generate_input_from_input_name(input_from_runs_by_input_name)
    raise Exception(
        "One of arguments [input_path, input_from_runs_by_run_id, input_from_runs_by_run_name, input_from_runs_by_input_name] need to be defined"
    )
