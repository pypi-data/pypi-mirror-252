from ..utils.utils import Utils


class FundraisingPage(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get(self, fundraising_page_id=None):
        return self._utils.get_resource(f"fundraising_pages/{fundraising_page_id}")

    def create(self, payload=None):
        return self._utils.post_resource(
            resource_name="fundraising_pages", resource_payload=payload
        )

    def update(self, fundraising_page_id=None, payload=None):
        return self._utils.update_resource(
            resource_name=f"fundraising_pages/{fundraising_page_id}",
            resource_payload=payload,
        )
