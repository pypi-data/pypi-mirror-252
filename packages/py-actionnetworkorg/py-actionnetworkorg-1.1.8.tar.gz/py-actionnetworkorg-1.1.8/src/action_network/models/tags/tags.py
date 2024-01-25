from ..utils.utils import Utils


class Tags(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get(self, page=None, per_page=25, limit=None, filter=None):
        if page:
            return self._utils.get_resource_collection("tags", limit, per_page, filter)
        return self._utils.get_resource_collection_paginated(
            "tags", per_page, page, filter
        )

    def create(self, tag_id, payloads=[]):
        return self._utils.post_resources(
            resource_name=f"tags/{tag_id}/taggings", resource_payloads=payloads
        )
