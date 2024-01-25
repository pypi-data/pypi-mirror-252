from ..utils.utils import Utils


class Donation(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get(self, donation_id=None):
        return self._utils.get_resource(f"donations/{donation_id}")

    def create(self, payload=None):
        return self._utils.post_resource(
            resource_name="donations", resource_payload=payload
        )

    def update(self, donation_id, payload=None):
        return self._utils.update_resource(
            resource_name=f"donations/{donation_id}", resource_payload=payload
        )
