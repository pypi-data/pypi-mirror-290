import requests as rq
from xml.etree import ElementTree

class UnasAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.token = None

    def get_unas_token(self):
        token_payload = f'<?xml version="1.0" encoding="UTF-8" ?><Params><ApiKey>{self.api_key}</ApiKey></Params>'
        token_request = rq.get("https://api.unas.eu/shop/login", data=token_payload)
        token_tree = ElementTree.fromstring(token_request.content)
        if token_tree[0].tag == "Token":
            self.token = token_tree[0].text
        return self.token

    def get_unas_feed_url(self, lang="hu"):
        if not self.token:
            self.get_unas_token()
        url_payload = f'<?xml version="1.0" encoding="UTF-8" ?><Params><Format>xlsx</Format><Lang>{lang}</Lang></Params>'
        url_request = rq.get(
            "https://api.unas.eu/shop/getProductDB",
            headers={"Authorization": f"Bearer {self.token}"},
            data=url_payload,
        )
        url_tree = ElementTree.fromstring(url_request.content)
        url = url_tree[0].text
        return url