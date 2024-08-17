import logging

import requests
from requests import Response
from cobroswap.models import CobrosWapJSON, ResponseCobrosWap

logger = logging.getLogger(__name__)

def url_create_payment_link() -> str:
    """ FIXME: Esto es genérico?"""
    return "https://cobroswap.com/api/banking/createExternalPayment"

def response_create_payment_link(*, cobroswap_json: CobrosWapJSON) -> Response:
    url = url_create_payment_link()
    return requests.post(url=url, json=cobroswap_json.model_dump())

def create_payment_link(*, cobroswap_json: CobrosWapJSON) -> ResponseCobrosWap | None:
    r = response_create_payment_link(cobroswap_json=cobroswap_json)
    if r.status_code == 201:
        return ResponseCobrosWap(**r.json())
    logger.warning(f"create_payment_link: status_code={r.status_code} | text={r.text}")
