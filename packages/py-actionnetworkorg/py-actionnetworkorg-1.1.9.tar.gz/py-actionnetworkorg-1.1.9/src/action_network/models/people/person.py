from ..utils.utils import Utils


class Person(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get(self, person_id=None):
        return self._utils.get_resource(f"people/{person_id}")
        return "Result"

    def create(self, payload=None):
        return self._utils.post_resource(
            resource_name=f"people", resource_payload=payload
        )

    def update(self, person_id=None, payload=None):
        return self._utils.post_resource(
            resource_name=f"people/{person_id}", resource_payload=payload
        )
