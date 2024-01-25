from ..utils.utils import Utils


class Wrapper(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get(self, wrapper_id=None):
        return self._utils.get_resource(f"wrappers/{wrapper_id}")

    def create(self, payload=None):
        return self._utils.post_resource(
            resource_name=f"wrappers", resource_payload=payload
        )

    def update(self, wrapper_id=None, payload=None):
        return self._utils.update_resource(
            resource_name=f"wrappers/{wrapper_id}", resource_payload=payload
        )