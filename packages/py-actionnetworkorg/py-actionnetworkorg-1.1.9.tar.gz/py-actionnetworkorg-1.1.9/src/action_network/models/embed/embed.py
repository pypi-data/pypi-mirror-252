from ..utils.utils import Utils


class Embed(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get(self, action_type=None, action_id=None):
        return self._utils.get_resource_collection_paginated(
            f"{action_type}/{action_id}/embed"
        )
