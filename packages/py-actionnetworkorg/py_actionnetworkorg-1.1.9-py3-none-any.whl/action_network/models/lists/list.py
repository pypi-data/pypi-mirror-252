from ..utils.utils import Utils


class List(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get(self, list_id=None):
        return self._utils.get_resource(f"lists/{list_id}")
