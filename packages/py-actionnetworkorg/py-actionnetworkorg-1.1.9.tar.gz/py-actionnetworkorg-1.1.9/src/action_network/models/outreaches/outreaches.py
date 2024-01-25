from ..utils.utils import Utils


class Outreaches(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get_by_advocacy_campaign(
        self, advocacy_campaign_id=None, page=None, per_page=25, limit=None, filter=None
    ):
        if page:
            return self._utils.get_resource_collection(
                f"advocacy_campaigns/{advocacy_campaign_id}/outreaches",
                limit,
                per_page,
                filter,
            )
        return self._utils.get_resource_collection_paginated(
            f"advocacy_campaigns/{advocacy_campaign_id}/outreaches",
            per_page,
            page,
            filter,
        )

    def get_by_person(
        self, person_id=None, page=None, per_page=25, limit=None, filter=None
    ):
        if page:
            return self._utils.get_resource_collection(
                f"people/{person_id}/outreaches", limit, per_page, filter
            )
        return self._utils.get_resource_collection_paginated(
            f"people/{person_id}/outreaches", per_page, page, filter
        )
        return "Result"

    def create(self, advocacy_campaign_id, payloads=[]):
        return self._utils.post_resources(
            resource_name=f"advocacy_campaigns/{advocacy_campaign_id}/outreaches",
            resource_payloads=payloads,
        )
