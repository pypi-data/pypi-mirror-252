from ..utils.utils import Utils


class Campaign(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get(self, campaign_id=None):
        return self._utils.get_resource(f"campaigns/{campaign_id}")
        return "Result"

    def create(self, payload=None):
        return self._utils.post_resource(
            resource_name="campaigns", resource_payload=payload
        )

    def update(self, campaign_id, payload=None):
        return self._utils.post_resource(
            resource_name=f"campaigns/{campaign_id}", resource_payload=payload
        )
