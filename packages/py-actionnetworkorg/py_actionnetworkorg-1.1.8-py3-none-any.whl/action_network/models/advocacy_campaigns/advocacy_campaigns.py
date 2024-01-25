from ..utils.utils import Utils


class AdvocacyCampaigns(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get(self, page=None, per_page=None, limit=None, filter=None):
        if page:
            return self._utils.get_resource_collection(
                "advocacy_campaigns", limit, per_page, filter
            )
        return self._utils.get_resource_collection_paginated(
            "advocacy_campaigns", per_page, page, filter
        )
        return "Result"

    def create(self, payloads=[]):
        return self._utils.post_resources(
            resource_name="advocacy_campaigns", resource_payloads=payloads
        )
