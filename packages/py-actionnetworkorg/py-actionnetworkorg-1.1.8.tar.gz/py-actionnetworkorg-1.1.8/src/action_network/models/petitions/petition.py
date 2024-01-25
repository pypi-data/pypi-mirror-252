from ..utils.utils import Utils


class Petition(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get(self, petition_id=None):
        return self._utils.get_resource(f"petitions/{petition_id}")

    def create(self, payload=None):
        return self._utils.post_resource(
            resource_name=f"petitions", resource_payload=payload
        )

    def update(self, petition_id=None, payload=None):
        return self._utils.update_resource(
            resource_name=f"petitions/{petition_id}", resource_payload=payload
        )
