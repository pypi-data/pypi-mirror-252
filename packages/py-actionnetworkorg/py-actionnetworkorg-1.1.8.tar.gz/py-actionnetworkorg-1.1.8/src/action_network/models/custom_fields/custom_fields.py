from ..utils.utils import Utils


class CustomFields(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get(self, page=None, per_page=25, limit=None, filter=None):
        return self.get_resource(
            "metadata/custom_fields", per_page, page, filter
        )
