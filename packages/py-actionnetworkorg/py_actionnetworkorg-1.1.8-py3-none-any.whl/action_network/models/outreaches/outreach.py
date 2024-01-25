from ..utils.utils import Utils


class Outreach(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get_by_advocacy_campaign(self, advocacy_campaign_id=None, outreach_id=None):
        return self._utils.get_resource(
            f"advocacy_campaigns/{advocacy_campaign_id}/outreaches/{outreach_id}"
        )

    def get_by_person(self, person_id=None, outreach_id=None):
        return self._utils.get_resource(f"people/{person_id}/outreaches/{outreach_id}")

    def create(self, advocacy_campaign_id=None, payload=None):
        return self._utils.post_resource(
            resource_name=f"advocacy_campaigns/{advocacy_campaign_id}/outreaches",
            resource_payload=payload,
        )

    def update(self, advocacy_campaign_id=None, outreach_id=None, payload=None):
        return self._utils.update_resource(
            resource_name=f"advocacy_campaigns/{advocacy_campaign_id}/outreaches/{outreach_id}",
            resource_payload=payload,
        )
