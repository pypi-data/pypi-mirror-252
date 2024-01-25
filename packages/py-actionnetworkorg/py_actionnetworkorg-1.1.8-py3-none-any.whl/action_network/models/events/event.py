from ..utils.utils import Utils


class Event(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get(self, event_id=None):
        return self._utils.get_resource(f"events/{event_id}")

    def create(self, payload=None):
        return self._utils.post_resource(resource_name="events")

    def update(self, event_id, payload=None):
        return self._utils.update_resource(
            resource_name=f"events/{event_id}", resource_payload=payload
        )
