from ..utils.utils import Utils


class Submission(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get_by_person(self, person_id=None, submission_id=None):
        return self._utils.get_resource(
            f"people/{person_id}/submissions/{submission_id}"
        )

    def get_by_form(self, form_id=None, submission_id=None):
        return self._utils.get_resource(f"forms/{form_id}/signatures/{submission_id}")

    def create(self, form_id, payload=None):
        return self._utils.post_resource(
            resource_name=f"forms/{form_id}/submissions", resource_payload=payload
        )

    def update(self, form_id, submission_id, payload=None):
        return self._utils.update_resource(
            resource_name=f"forms/{form_id}/submissions/{submission_id}",
            resource_payload=payload,
        )
