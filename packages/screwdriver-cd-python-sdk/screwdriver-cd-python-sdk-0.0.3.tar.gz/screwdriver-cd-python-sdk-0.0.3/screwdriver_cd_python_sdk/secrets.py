import logging
import requests
import sys, os

logging.basicConfig(level=logging.DEBUG)

def _headers(token: str) -> object:
    return {
        'accept': 'application/json',
        'Authorization': token,
        'Content-Type': 'application/json',
    }


def create_or_update_secret(secret_name: str, secret_value: str, pipeline_id: int, token: str) -> None:
    """
    "allowInPR" is set to be false by default

    :param secret_name:
    :param secret_value:
    :param pipeline_id:
    :param token:
    """

    response = requests.get(
        "http://10.8.0.6:9001/v4/pipelines/{}/secrets".format(pipeline_id),
        headers={
            'accept': 'application/json',
            'Authorization': token,
        }
    )
    if secret_name in str(response.content):
        logging.debug("Updating secret '{}'".format(secret_name))

        for secrete in response.json():
            if secrete["name"] == secret_name:
                json_data = {
                    'value': secret_value,
                    'allowInPR': False,
                }

                if requests.put('http://10.8.0.6:9001/v4/secrets/{}'.format(secrete["id"]), headers=_headers(token), json=json_data).status_code != 200:
                    sys.exit(os.EX_CONFIG)
    else:
        logging.debug("Creating secret '{}'".format(secret_name))

        json_data = {
            'pipelineId': pipeline_id,
            'name': secret_name,
            'value': secret_value,
            'allowInPR': False,
        }

        if requests.post('http://10.8.0.6:9001/v4/secrets', headers=_headers(token), json=json_data).status_code != 201:
            sys.exit(os.EX_CONFIG)
