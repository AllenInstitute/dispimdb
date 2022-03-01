import posixpath

import ddbclient.base
from ddbclient import utils


class SessionClient(ddbclient.base.BaseClient):
    def get_sessions_from_specimen(self, specimen_id):
        url = posixpath.join(
            self.base_url,
            f"specimen/{specimen_id}/sessions")
        return utils.get_json(url)

    def get_session(self, specimen_id, session_id):
        url = posixpath.join(
            self.base_url,
            f"specimen/{specimen_id}/session/{session_id}")
        return utils.get_json(url)
