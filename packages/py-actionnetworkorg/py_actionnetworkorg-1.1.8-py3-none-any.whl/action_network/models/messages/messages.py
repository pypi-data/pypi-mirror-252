from ..utils.utils import Utils


class Messages(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get(self, page=None, per_page=25, limit=None, filter=None):
        if page:
            return self._utils.get_resource_collection(
                "messages", limit, per_page, filter
            )
        return self._utils.get_resource_collection_paginated(
            "messages", per_page, page, filter
        )

    def create(self, payloads=[]):
        return self._utils.post_resources(
            resource_name="messages", resource_payloads=payloads
        )
