from cleora_saas_api.api.dto_keys import INPUT_HASH, INPUT_NAME, INPUT_PATH, MEMORY


class InputFileDetails:
    is_local_file = True

    def __init__(
        self,
        input_name,
        input_path,
        memory,
        input_hash,
    ):
        self.input_name = input_name
        self.input_path = input_path
        self.memory = memory
        self.input_hash = input_hash
        self.is_local_file = False

    def get_input_details_dict(self):
        return {
            INPUT_PATH: self.input_path,
            INPUT_NAME: self.input_name,
            MEMORY: self.memory,
            INPUT_HASH: self.input_hash,
        }

    def set_is_local_file(self, is_local: bool):
        self.is_local_file = is_local
