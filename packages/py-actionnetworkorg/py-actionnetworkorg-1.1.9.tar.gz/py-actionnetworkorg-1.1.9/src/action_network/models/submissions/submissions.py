from ..utils.utils import Utils


class Submissions(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get_by_person(
        self, person_id=None, page=None, per_page=25, limit=None, filter=None
    ):
        if page:
            return self._utils.get_resource_collection(
                f"people/{person_id}/submissions", limit, per_page, filter
            )
        return self._utils.get_resource_collection_paginated(
            f"people/{person_id}/submissions", per_page, page, filter
        )

    def get_by_form(
        self, form_id=None, page=None, per_page=25, limit=None, filter=None
    ):
        if page:
            return self._utils.get_resource_collection(
                f"forms/{form_id}/submissions", limit, per_page, filter
            )
        return self._utils.get_resource_collection_paginated(
            f"forms/{form_id}/submissions", per_page, page, filter
        )

    def create(self, form_id, payloads=[]):
        return self._utils.post_resources(
            resource_name=f"forms/{form_id}/submissions", resource_payloads=payloads
        )
