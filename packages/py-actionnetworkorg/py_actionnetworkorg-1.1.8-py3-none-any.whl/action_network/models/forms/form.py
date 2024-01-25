from ..utils.utils import Utils


class Form(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get(self, form_id=None):
        return self._utils.get_resource(f"forms/{form_id}")

    def create(self, payload=None):
        return self._utils.post_resource(
            resource_name="forms", resource_payload=payload
        )

    def update(self, form_id=None, payload=None):
        return self._utils.update_resource(f"forms/{form_id}", resource_payload=payload)
