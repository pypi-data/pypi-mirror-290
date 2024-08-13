from cleora_saas_api.api.dto_keys import ID_TOKEN, REFRESH_TOKEN
from cleora_saas_api.token.token_managment import get_auth, save_new_tokens_to_file
from cleora_saas_api.token.token_model import Tokens


def login_by_custom_token(custom_token):
    auth = get_auth()
    credentials = auth.sign_in_with_custom_token(custom_token)
    tokens = Tokens(credentials[ID_TOKEN], credentials[REFRESH_TOKEN])
    save_new_tokens_to_file(tokens)