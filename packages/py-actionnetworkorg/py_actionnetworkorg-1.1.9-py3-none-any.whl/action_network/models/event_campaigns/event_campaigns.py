from ..utils.utils import Utils


class EventCampaigns(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    @property
    def get(self, page=None, per_page=25, limit=None, filter=None):
        if page:
            return self._utils.get_resource_collection(
                "event_campaigns", limit, per_page, filter
            )
        return self._utils.get_resource_collection_paginated(
            "event_campaigns", per_page, page, filter
        )

    def create(self, payload=None):
        return self._utils.post_resource(
            resource_name="event_campaigns", resource_payload=payload
        )
