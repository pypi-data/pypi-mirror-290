import json
import requests
import urllib3

from cleora_saas_api.api.api_endpoints_adresses import (
    ADRESS_TO_GET_RUN_INFO,
    ADRESS_TO_GET_RUNS,
    ADRESS_TO_GET_TRIGGER_BODY,
    ADRESS_TO_PREPARE_RUN,
    ADRESS_TO_TRIGGER_RUN,
)

urllib3.disable_warnings()

pool = urllib3.HTTPSConnectionPool(
    "europe-west1-monad-test-361009.cloudfunctions.net",
    assert_hostname="cloudfunctions.net",
)

requests.packages.urllib3.disable_warnings()


def trigger_argo(body, id_token):
    trigger_argo_response = requests.post(
        ADRESS_TO_TRIGGER_RUN,
        data=rf"{json.dumps(body)}",
        headers={
            "content-type": "application/json",
            "authorization": f"Bearer {id_token}",
        },
        verify=False,
    )
    return trigger_argo_response


def call_cloud_function(adress_url, body, id_token):
    response = requests.post(
        adress_url,
        data=rf"{json.dumps(body)}",
        headers={
            "content-type": "application/json",
            "authorization": f"Bearer {id_token}",
        },
        verify=False,
    )
    return response


def prepare_run(body, id_token):
    return call_cloud_function(ADRESS_TO_PREPARE_RUN, body, id_token)


def trigger_run(body, id_token):
    return call_cloud_function(ADRESS_TO_TRIGGER_RUN, body, id_token)


def get_trigger_body(body, id_token):
    response = call_cloud_function(ADRESS_TO_GET_TRIGGER_BODY, body, id_token)
    if not response.ok:
        raise Exception(response.text)
    return response.json()


def get_run_info(body, id_token):
    response = call_cloud_function(ADRESS_TO_GET_RUN_INFO, body, id_token)
    if not response.ok:
        raise Exception(response.text)
    return response.json()


def get_runs(id_token):
    runs_response = call_cloud_function(ADRESS_TO_GET_RUNS, {}, id_token)
    if not runs_response.ok:
        raise Exception(runs_response.text)
    return runs_response.json()
