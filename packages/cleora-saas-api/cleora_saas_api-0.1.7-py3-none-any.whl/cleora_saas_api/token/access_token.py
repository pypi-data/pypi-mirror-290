import requests
from cleora_saas_api.config import FIREBASE_CONFIG, STORAGE_ROOT
from cleora_saas_api.token.remove_query_params import remove_query_params_from_url
from cleora_saas_api.token.token_managment import get_id_token
import pyrebase


def get_access_token(external_path:str):
    try:
        id_token = get_id_token()
        firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
        storage = firebase.storage()
        external_path = external_path.replace(STORAGE_ROOT, "")

        url = remove_query_params_from_url(storage.child(external_path).get_url(None))
        header = {"Authorization": "Bearer " + id_token}
        response = requests.get(url, headers=header)
        access_tk = response.json()["downloadTokens"]
        return access_tk
    except Exception as exception:
        print("Something go wrong access token generation. Please try again.")
