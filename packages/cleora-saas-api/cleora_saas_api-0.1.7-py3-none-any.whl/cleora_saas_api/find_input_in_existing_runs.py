from pathlib import Path
from cleora_saas_api.api.dto_keys import INPUT_HASH, INPUT_NAME, INPUT_PATH, MEMORY, NAME
from cleora_saas_api.file_hash import get_file_hash
from cleora_saas_api.input_details.input_file_details import InputFileDetails



def build_is_key_in_object(key: str):
    return lambda obj: key in obj.keys()


def find_input_in_existing_runs(input_path, runs):
    inputFileName = Path(input_path).name
    runs_with_hash = filter(build_is_key_in_object(INPUT_HASH), runs)

    for run in runs_with_hash:
        if inputFileName == run[INPUT_NAME]:
            file_hash = get_file_hash(input_path)
            file_hash_from_database = run[INPUT_HASH]
            if file_hash == file_hash_from_database:
                input_file_details = InputFileDetails(
                    input_name=run[INPUT_NAME],
                    input_path=run[INPUT_PATH],
                    memory=run[MEMORY],
                    input_hash=file_hash_from_database,
                )
                return input_file_details
    return None

def find_input_in_existing_runs_by_input_name(input_name, runs):
    runs_with_hash = filter(build_is_key_in_object(INPUT_HASH), runs)
    for run in runs_with_hash:
        if input_name == run[INPUT_NAME]:
            file_hash_from_database = run[INPUT_HASH]
            input_file_details = InputFileDetails(
                input_name=run[INPUT_NAME],
                input_path=run[INPUT_PATH],
                memory=run[MEMORY],
                input_hash=file_hash_from_database,
            )
            return input_file_details
    return None

def find_input_in_existing_runs_by_run_name(run_name, runs):
    for run in runs:
        if run_name == run[NAME]:
            file_hash_from_database = run[INPUT_HASH]
            input_file_details = InputFileDetails(
                input_name=run[INPUT_NAME],
                input_path=run[INPUT_PATH],
                memory=run[MEMORY],
                input_hash=file_hash_from_database,
            )
            return input_file_details
    return None
