import os
from cleora_saas_api.token.access_token import get_access_token
import pyrebase

from cleora_saas_api.config import FIREBASE_CONFIG, STORAGE_ROOT


def download_file(external_path: str, local_path: str, id_token):
    print("-- Result download started --")
    firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
    storage = firebase.storage()
    external_path = external_path.replace(STORAGE_ROOT, "")

    access_tk = get_access_token(external_path)

    path = os.path.dirname(local_path)
    # Note: The full local path is assigned to the filename because there is a bug in the Pyrebase library that ignores the path argument
    storage.child(external_path).download(filename=local_path, path=path, token=access_tk)

    print("-- Result download finished --")
