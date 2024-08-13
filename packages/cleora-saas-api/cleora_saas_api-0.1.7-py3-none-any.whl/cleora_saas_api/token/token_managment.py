import os
import pathlib
import shutil
import time
import pyrebase
import jwt

from cleora_saas_api.config import (
    FIREBASE_CONFIG,
    ID_TOKEN_FILE_NAME,
    REFRESH_TOKEN_FILE_NAME,
    CLEORA_CREDENTIALS_FOLDER_NAME,
)
from cleora_saas_api.token.token_model import Tokens


def root_path():
    return pathlib.Path(pathlib.Path.home(), CLEORA_CREDENTIALS_FOLDER_NAME)


def get_auth():
    firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
    auth = firebase.auth()
    return auth


def read_id_token_from_file():
    with open(pathlib.Path(root_path(), ID_TOKEN_FILE_NAME), "r") as f:
        return f.read()


def read_refresh_token_from_file():
    with open(pathlib.Path(root_path(), REFRESH_TOKEN_FILE_NAME), "r") as f:
        return f.read()


def is_id_token_expired():
    try:
        id_token = read_id_token_from_file()
        header_data = jwt.get_unverified_header(id_token)
        jwt_decoded = jwt.decode(
            id_token, options={"verify_signature": False}, algorithms=header_data["alg"]
        )
        expired_date = jwt_decoded["exp"]

        currnent_time = time.time()
        return currnent_time > expired_date
    except Exception as exception:
        print("Somthing go wrong during decoding your token. Please login once again.")


def get_new_id_tokens() -> Tokens:
    refresh_token = read_refresh_token_from_file()
    firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
    auth = firebase.auth()
    credentials = auth.refresh(refresh_token)
    tokens = Tokens(credentials["idToken"], credentials["refreshToken"])
    return tokens


def save_new_tokens_to_file(tokens: Tokens):
    pathlib.Path(root_path()).mkdir(parents=True, exist_ok=True)
    path_to_refresh_token = pathlib.Path(root_path(), REFRESH_TOKEN_FILE_NAME)
    path_to_id_token = pathlib.Path(root_path(), ID_TOKEN_FILE_NAME)
    with open(path_to_refresh_token, "w") as refresh_file:
        refresh_file.write(tokens.refresh_token)
    with open(path_to_id_token, "w") as id_token_file:
        id_token_file.write(tokens.id_token)
    pass


def remove_credentails_folder():
    credential_path = pathlib.Path(root_path())
    if credential_path.is_dir():
        shutil.rmtree(credential_path)
    return "Credentials removed"


def get_id_token():
    try:
        token_expired = is_id_token_expired()
        if (
            token_expired or True
        ):  # This force to get always new token based on refresh token. So if refresh token will be revoked the effect will be immediate.
            tokens = get_new_id_tokens()
            save_new_tokens_to_file(tokens)
            return tokens.id_token
        return read_id_token_from_file()
    except Exception as exception:
        print("Something get wrong with your credentials. Please login once again.")


def check_if_credentials_exists() -> bool:
    if not os.path.exists(str(pathlib.Path(root_path()))):
        return False
    is_id_token = os.path.isfile(pathlib.Path(root_path(), ID_TOKEN_FILE_NAME))
    is_refresh_token = os.path.isfile(pathlib.Path(root_path(), ID_TOKEN_FILE_NAME))
    return is_id_token and is_refresh_token


def check_login_status_with_showing_message():
    if not check_if_credentials_exists():
        print("Please login first")
        return
    return True
