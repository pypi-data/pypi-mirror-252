from ..utils.utils import Utils


class Lists(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get(self, page=None, per_page=25, limit=None, filter=None):
        if page:
            return self._utils._get_resource_collection(
                f"lists", limit, per_page, filter
            )
        return self._utils._get_resource_collection_paginated(
            f"lists", per_page, page, filter
        )
