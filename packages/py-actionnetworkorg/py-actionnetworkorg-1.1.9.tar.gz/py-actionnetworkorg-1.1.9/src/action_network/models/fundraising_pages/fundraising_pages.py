from ..utils.utils import Utils


class FundraisingPages(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get(self, page=None, per_page=25, limit=None, filter=None):
        if page:
            return self._utils.get_resource_collection(
                "fundraising_pages", limit, per_page, filter
            )
        return self._utils.get_resource_collection_paginated(
            "fundraising_pages", per_page, page, filter
        )

    def create(self, payloads=[]):
        return self._utils.post_resource(
            resource_name="fundraising_pages", resource_payloads=payloads
        )
