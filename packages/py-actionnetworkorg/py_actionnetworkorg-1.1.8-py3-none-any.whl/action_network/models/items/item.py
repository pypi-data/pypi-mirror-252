from ..utils.utils import Utils


class Item(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get_by_list(self, list_id=None, item_id=None):
        return self._utils.get_resource(f"lists/{list_id}/items/{item_id}")
