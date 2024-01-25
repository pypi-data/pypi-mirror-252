from ..utils.utils import Utils

class Query(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get(self, query_id=None):
        return self._utils.get_resource(f"queries/{query_id}")

    def create(self, payload=None):
        return self._utils.post_resource(
            resource_name=f"queries", resource_payload=payload
        )

    def update(self, query_id=None, payload=None):
        return self._utils.update_resource(
            resource_name=f"queries/{query_id}", resource_payload=payload
        )
