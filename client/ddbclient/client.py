from ddbclient import (
    acquisition, specimen, session, section)


class DispimDbClient:
    def __init__(self, base_url=None):
        self.base_url = base_url

        self._register_client("acquisition", acquisition.AcquisitionClient)
        self._register_client("specimen", specimen.SpecimenClient)
        self._register_client("session", session.SessionClient)
        self._register_client("section", section.SectionClient)

    def _register_client(self, client_name, client_class):
        client_obj = client_class(**{
            "base_url": self.base_url})
        setattr(self, client_name, client_obj)
