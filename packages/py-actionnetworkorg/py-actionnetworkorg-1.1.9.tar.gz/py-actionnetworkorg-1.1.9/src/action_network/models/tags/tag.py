from ..utils.utils import Utils


class Tag(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get(self, tag_id=None):
        return self._utils.get_resource(f"tags/{tag_id}")

    def create(self, payload=None):
        return self._utils.post_resource(
            resource_name=f"tags", resource_payload=payload
        )

    def update(self, tag_id=None, payload=None):
        return self._utils.post_resource(
            resource_name=f"tags/{tag_id}", resource_payload=payload
        )
