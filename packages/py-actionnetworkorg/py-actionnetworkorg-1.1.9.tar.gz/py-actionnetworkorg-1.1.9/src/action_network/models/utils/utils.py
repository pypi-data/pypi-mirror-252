import requests
import json


class Utils:
    _instance = None

    def __new__(cls, headers):
        if cls._instance is None:
            cls._instance = super(Utils, cls).__new__(cls)
            cls._instance.init_instance(headers=headers)
        return cls._instance

    def init_instance(self, headers):
        self._base_url = "https://actionnetwork.org/api/v2/"
        self._headers = headers

    def get_resource_collection(
        self, resource_name, limit=None, per_page=25, filter=None
    ):
        count = 0
        results = []
        page = 1
        while True:
            url = (
                self._base_url
                + f"{resource_name}/?page={page}&per_page={per_page}filter={filter}"
            )
            response = requests.get(url, headers=self._headers)
            response_json = json.loads(response.text)
            count += len(
                response_json["_embedded"][list(response_json["_embedded"])[0]]
            )
            results.append(
                response_json["_embedded"][list(response_json["_embedded"])[0]]
            )
            page += 1
            if not (
                count < response_json["total_records"]
                or (limit != None and count < limit)
            ):
                break
        return results

    def get_resource_collection_paginated(
        self, resource_name, per_page=25, page=None, filter=None
    ):
        url = (
            self._base_url
            + f"{resource_name}/?page={page}&per_page={per_page}filter={filter}"
        )
        response = requests.get(url, headers=self._headers)
        response_json = json.loads(response.text)
        return response_json

    def get_resource(self, resource_name):
        url = self._base_url + resource_name
        response = requests.get(url, headers=self._headers)
        response_json = json.loads(response.text)
        return response_json

    def post_resource(self, resource_name, resource_payload):
        url = self._base_url + resource_name
        response = requests.post(
            url, headers=self._headers, data=json.dumps(resource_payload)
        )
        response_json = json.loads(response.text)
        return response_json

    def update_resource(self, resource_name, resource_payload):
        url = self._base_url + resource_name
        response = requests.put(
            url, headers=self._headers, data=json.dumps(resource_payload)
        )
        response_json = json.loads(response.text)
        return response_json

    def post_resources(self, resource_name, resource_payloads):
        results = []
        for payload in resource_payloads:
            response = self.post_resource(
                resource_name=resource_name, resource_payload=payload
            )
            results.append(response)
        return results
