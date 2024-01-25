from ..utils.utils import Utils


class Signature(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get_by_person(self, person_id=None, signature_id=None):
        return self._utils.get_resource(f"people/{person_id}/signatures/{signature_id}")

    def get_by_petition(self, petition_id=None, signature_id=None):
        return self._utils.get_resource(
            f"petitions/{petition_id}/signatures/{signature_id}"
        )

    def create(self, petition_id, payload=None):
        return self._utils.post_resource(
            resource_name=f"petitions/{petition_id}/signatures",
            resource_payload=payload,
        )

    def update(self, petition_id, signature_id, payload=None):
        return self._utils.update_resource(
            resource_name=f"petitions/{petition_id}/signatures/{signature_id}",
            resource_payload=payload,
        )
