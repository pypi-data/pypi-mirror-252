from ..utils.utils import Utils


class Attendances(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get_by_person(
        self, person_id=None, page=None, per_page=25, limit=None, filter=None
    ):
        if page:
            return self._utils.get_resource_collection(
                f"people/{person_id}/attendances", limit, per_page, filter
            )
        return self._utils.get_resource_collection_paginated(
            f"people/{person_id}/attendances", per_page, page, filter
        )

    def get_by_event(
        self, event_id=None, page=None, per_page=25, limit=None, filter=None
    ):
        if page:
            return self._utils.get_resource_collection(
                f"events/{event_id}/attendances", limit, per_page, filter
            )
        return self._utils.get_resource_collection_paginated(
            f"events/{event_id}/attendances", per_page, page, filter
        )

    def create(self, payloads=[]):
        return self._utils.post_resources(
            resource_name=f"events", resource_payloads=payloads
        )
