from ..utils.utils import Utils


class EventCampaign(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get(self, event_campaign_id=None):
        return self._utils.get_resource(f"event_campaigns/{event_campaign_id}")

    def create(self, payload=None):
        return self._utils.update_resource(
            resource_name="event_campaigns", resource_payload=payload
        )

    def update(self, event_campaign_id, payloads=[]):
        return self._utils.update_resources(
            resource_name=f"event_campaigns/{event_campaign_id}",
            resource_payloads=payloads,
        )
