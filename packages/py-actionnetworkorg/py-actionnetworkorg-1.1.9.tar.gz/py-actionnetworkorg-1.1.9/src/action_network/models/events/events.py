from ..utils.utils import Utils


class Events(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get_by_event_campaign(
        self, event_campaign_id=None, page=None, per_page=25, limit=None, filter=None
    ):
        if page:
            return self._get_resource_collection(
                f"event_campaigns/{event_campaign_id}/events", limit, per_page, filter
            )
        return self._get_resource_collection_paginated(
            f"event_campaigns/{event_campaign_id}/events", per_page, page, filter
        )

    def get(self, page=None, per_page=25, limit=None, filter=None):
        if page:
            return self._utils.get_resource_collection(
                f"events", limit, per_page, filter
            )
        return self._utils.get_resource_collection_paginated(
            f"events", per_page, page, filter
        )

    def create(self, payloads=[]):
        return self._utils.post_resources(
            resource_name="events", resource_payloads=payloads
        )
