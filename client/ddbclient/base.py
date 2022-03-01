import posixpath


class BaseClient:
    def __init__(self,
                 base_url=None,
                 hostname=None,
                 port=None,
                 subpath=None):
        """
        Parameters
        ----------
        base_url : str
            Base url of the api (e.g. http://bigkahuna.corp.alleninstitute.org/api)
        hostname : str
            Name of API host (e.g. http://bigkahuna.corp.alleninstitute.org)
        port : str
            Port number for API (e.g. 8000)
        subpath : str
            Specifies path to api and version (e.g. 'api/v1')
        """
        self.base_url = base_url
        self.hostname = hostname
        self.port = port
        self.subpath = subpath

        if self.port is not None:
            self.hostname = self.hostname + ':' + self.port

        if self.base_url is None:
            self.base_url = posixpath.join(
                self.hostname,
                self.subpath
            )
        else:
            self.base_url = posixpath.join(
                self.base_url,
                self.subpath
            )
