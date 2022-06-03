class BaseClient:
    def __init__(self, base_url=None):
        """
        Parameters
        ----------
        base_url : str
            Base url of the api (e.g. http://bigkahuna.corp.alleninstitute.org/api)
        """
        self.base_url = base_url
