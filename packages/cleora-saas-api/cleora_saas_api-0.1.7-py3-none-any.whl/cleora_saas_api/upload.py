import pyrebase

from cleora_saas_api.config import FIREBASE_CONFIG, STORAGE_ROOT

def upload_file(localPath: str, externalPath: str, id_token):
    print("-- File uploading started --")
    firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
    storage = firebase.storage()
    externalPath = externalPath.replace(STORAGE_ROOT, "")
    storage.child(externalPath).put(localPath, id_token)
    print("-- File uploading finished --")