import posixpath

import ddbclient.base
from ddbclient import utils


class SpecimenClient(ddbclient.base.BaseClient):
    def get_specimens(self):
        url = posixpath.join(
            self.base_url,
            "specimens")
        return utils.get_json(url)

    def get_specimen(self, specimen_id):
        url = posixpath.join(
            self.base_url,
            f"specimen/{specimen_id}")
        return utils.get_json(url)
