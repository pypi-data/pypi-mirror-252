from ..utils.utils import Utils


class Donations(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get_by_person(
        self, person_id=None, page=None, per_page=25, limit=None, filter=None
    ):
        if page:
            return self._utils.get_resource_collection(
                f"people/{person_id}/donations", limit, per_page, filter
            )
        return self._utils.get_resource_collection_paginated(
            f"people/{per_page}/donations", per_page, page, filter
        )
        return "Result"

    def get_by_fundraising_page(
        self, fundraising_page_id=None, page=None, per_page=25, limit=None, filter=None
    ):
        if page:
            return self._utils.get_resource_collection(
                f"fundraising_page_id/{fundraising_page_id}/donations",
                limit,
                per_page,
                filter,
            )
        return self._utils.get_resource_collection_paginated(
            f"fundraising_page_id/{fundraising_page_id}/donations",
            per_page,
            page,
            filter,
        )

    def get(self, page=None, per_page=25, limit=None, filter=None):
        if page:
            return self._utils.get_resource_collection(
                "donations", limit, per_page, filter
            )
        return self._utils.get_resource_collection_paginated(
            "donations", per_page, page, filter
        )

    def create(self, payloads=[]):
        return self._utils.update_resources(
            resource_name=f"donations", resource_payloads=payloads
        )
