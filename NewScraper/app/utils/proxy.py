import requests
from urllib.parse import urlencode
from app.utils import timing

def get_proxy_response(url, api_key):
    proxy_params = {
        "api_key": api_key,
        "url": url,
    }

    response = requests.get(
        url="https://proxy.scrapeops.io/v1/",
        params=urlencode(proxy_params),
    )
    return response