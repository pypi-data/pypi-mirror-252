import logging
import requests
import sys, os


def create_pipeline(checkout_url: str, screwdriver_api_url: str, token: str, source_directory=None) -> None:
    """
    Creates a new Screwdriver pipeline for a particular repo and an optional source directory.

    If the source_directory is not specified, it defaults to the repo root.

    :param checkout_url:
    :param screwdriver_api_url:
    :param token:
    :param source_directory:
    """
    logging.debug("Creating pipeline '{}/{}'".format(checkout_url, source_directory if source_directory else "root"))

    headers = {
        'accept': 'application/json',
        'Authorization': token,
        'Content-Type': 'application/json',
    }

    json_data = {
        'checkoutUrl': checkout_url,
        'rootDir': source_directory,
        'autoKeysGeneration': True,
    } if source_directory else {
        'checkoutUrl': checkout_url,
        'autoKeysGeneration': True,
    }

    response = requests.post('{}/v4/pipelines'.format(screwdriver_api_url), headers=headers, json=json_data)

    if response.status_code != 201:
        sys.exit(os.EX_CONFIG)

    return response.json()


def get_pipeline_id(pipeline_name: str, screwdriver_api_url: str, token: str) -> int:
    headers = {
        'accept': 'application/json',
        'Authorization': token,
    }

    params = {
        'page': '1',
        'count': '50',
        'search': pipeline_name,
        'sort': 'descending',
    }

    response = requests.get('{}/v4/pipelines'.format(screwdriver_api_url), params=params, headers=headers)

    if response.status_code != 200:
        logging.error("Getting pipeline ID: {} not found".format(pipeline_name))
        sys.exit(os.EX_CONFIG)

    for match in response.json():
        if match["name"] == pipeline_name:
            return match["id"]

    sys.exit(os.EX_CONFIG)
