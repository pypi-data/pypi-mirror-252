from ..utils.utils import Utils


class Signatures(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get_by_person(
        self, person_id=None, page=None, per_page=25, limit=None, filter=None
    ):
        if page:
            return self._utils.get_resource_collection(
                f"people/{person_id}/signatures", limit, per_page, filter
            )
        return self._utils.get_resource_collection_paginated(
            f"people/{person_id}/signatures", per_page, page, filter
        )

    def get_by_petition(
        self, petition_id=None, page=None, per_page=25, limit=None, filter=None
    ):
        if page:
            return self._utils.get_resource_collection(
                f"petitions/{petition_id}/signatures", limit, per_page, filter
            )
        return self._utils.get_resource_collection_paginated(
            f"petitions/{petition_id}/signatures", per_page, page, filter
        )

    def create(self, petition_id, payloads=[]):
        return self._utils.post_resources(
            resource_name=f"petitions/{petition_id}/signatures",
            resource_payloads=payloads,
        )
