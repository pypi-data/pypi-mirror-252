from ..utils.utils import Utils


class Tagging(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get_by_tag(self, tag_id=None, tagging_id=None):
        return self._utils.get_resource(f"tags/{tag_id}/taggings/{tagging_id}")

    def create(self, tag_id, payload=None):
        return self._utils.post_resource(
            resource_name=f"tags/{tag_id}/taggings", resource_payload=payload
        )

    def update(self, tag_id, tagging_id, payload=None):
        return self._utils.update_resource(
            resource_name=f"tags/{tag_id}/taggings/{tagging_id}",
            resource_payload=payload,
        )
