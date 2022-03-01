from ddbclient import (
    acquisition, specimen, session, section)


class DispimDbClient:
    def __init__(self,
                 base_url=None,
                 hostname=None,
                 port=None,
                 subpath=None):
        self.base_url = base_url
        self.hostname = hostname
        self.port = port
        self.subpath = subpath

        self._register_client("acquisition", acquisition.AcquisitionClient)
        self._register_client("specimen", specimen.SpecimenClient)
        self._register_client("session", session.SessionClient)
        self._register_client("section", section.SectionClient)

    def _register_client(self, client_name, client_class):
        client_obj = client_class(**{
            "base_url": self.base_url,
            "hostname": self.hostname,
            "port": self.port,
            "subpath": self.subpath})
        setattr(self, client_name, client_obj)
