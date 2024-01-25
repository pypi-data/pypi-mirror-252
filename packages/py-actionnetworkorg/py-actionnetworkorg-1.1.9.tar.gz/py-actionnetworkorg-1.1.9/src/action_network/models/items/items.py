from ..utils.utils import Utils


class Items(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get_by_list(
        self, list_id=None, page=None, per_page=25, limit=None, filter=None
    ):
        if page:
            return self._utils.get_resource_collection_paginated(
                f"lists/{list_id}/items", per_page, page, filter
            )
        return self._utils.get_resource_collection(
            f"lists/{list_id}/items", limit, per_page, filter
        )
