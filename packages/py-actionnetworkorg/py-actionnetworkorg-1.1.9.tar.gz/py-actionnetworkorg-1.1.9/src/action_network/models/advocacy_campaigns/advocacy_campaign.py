from ..utils.utils import Utils

class AdvocacyCampaign(object):
    def __init__(self, headers):
        self._utils = Utils(headers)
        self._headers = headers

    def get(self, advocacy_campaign_id=None):
        return self._utils.get_resource(f"advocacy_campaigns/{advocacy_campaign_id}")

    def create(self, payload=None):
        return self._utils.post_resource(
            resource_name="advocacy_campaigns", resource_payload=payload
        )

    def update(self, advocacy_campaign_id, payload=None):
        return self._utils.update_resource(
            resource_name=f"advocacy_campaigns/{advocacy_campaign_id}",
            resource_payload=payload,
        )
