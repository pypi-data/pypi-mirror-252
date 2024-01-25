from ..utils.utils import Utils


class Attendance(object):
    def __init__(self, headers):
        self._headers = headers
        self._utils = Utils(headers=headers)

    def get_by_event(self, event_id, attendance_id=None):
        return self._utils.get_resource(
            f"events/{event_id}/attendances/{attendance_id}"
        )

    def get_by_person(self, person_id, attendance_id=None):
        return self._utils.get_resource(
            f"people/{person_id}/attendances/{attendance_id}"
        )

    def create(self, event_id, payload=None):
        return self._utils.post_resource(
            resource_name=f"events/{event_id}/attendances", resource_payload=payload
        )

    def update(self, event_id, attendance_id, payload=None):
        return self._utils.update_resource(
            resource_name=f"events/{event_id}/attendances/{attendance_id}",
            resource_payload=payload,
        )
