from cleora_saas_api.token.token_managment import (
    get_new_id_tokens,
    save_new_tokens_to_file,
)
from cleora_saas_api.token.token_model import Tokens


def login_by_refresh_token(refresh_token):
    try:
        tokens = Tokens(id_token="", refresh_token=refresh_token)
        save_new_tokens_to_file(tokens)
        new_tokens = get_new_id_tokens()
        save_new_tokens_to_file(new_tokens)
    except Exception as exception:
        print("Something go wrong with login. Please copy again your token from app.")
        raise exception
