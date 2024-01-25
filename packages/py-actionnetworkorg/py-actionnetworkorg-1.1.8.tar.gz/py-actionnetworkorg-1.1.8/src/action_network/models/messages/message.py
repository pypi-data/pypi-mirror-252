from ..utils.utils import Utils


class Message(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get(self, message_id=None):
        return self._utils.get_resource(f"messages/{message_id}")

    def create(self, payload=None):
        return self._utils.post_resource(
            resource_name="messages", resource_payload=payload
        )

    def update(self, message_id, payload=None):
        return self._utils.update_resource(
            resource_name=f"messages/{message_id}", resource_payload=payload
        )
