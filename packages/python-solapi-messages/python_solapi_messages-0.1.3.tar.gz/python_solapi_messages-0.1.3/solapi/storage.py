import base64

import requests

from solapi.auth import get_headers
from solapi.config import SolApiConfig


def upload_image(path: str, config: SolApiConfig) -> requests.Response:
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    data = {"file": str(encoded_string)[2:-1], "type": "MMS"}
    headers = get_headers(config.api_key, config.secret_key)
    return requests.post(config.get_url("/storage/v1/files"), headers=headers, json=data)


def upload_rcs_image(path: str, config: SolApiConfig) -> requests.Response:
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    data = {"file": str(encoded_string)[2:-1], "type": "RCS"}
    headers = get_headers(config.api_key, config.secret_key)
    return requests.post(config.get_url("/storage/v1/files"), headers=headers, json=data)


def upload_kakao_image(path: str, config: SolApiConfig) -> requests.Response:
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    data = {"file": str(encoded_string)[2:-1], "type": "KAKAO"}
    headers = get_headers(config.api_key, config.secret_key)
    return requests.post(config.get_url("/storage/v1/files"), headers=headers, json=data)