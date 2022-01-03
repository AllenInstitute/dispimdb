import requests

from ddbclient import acquisition

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
        
        self.acquisition = acquisition.AcquisitionClient(
            base_url=self.base_url,
            hostname=self.hostname,
            port=self.port,
            subpath=self.subpath
        )