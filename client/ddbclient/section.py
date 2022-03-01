import posixpath

import ddbclient.base
from ddbclient import utils


class SectionClient(ddbclient.base.BaseClient):
    def get_sections_from_specimen(self, specimen_id):
        url = posixpath.join(
            self.base_url,
            f"specimen/{specimen_id}/sections")
        return utils.get_json(url)

    def get_section(self, specimen_id, section_num):
        url = posixpath.join(
            self.base_url,
            f"specimen/{specimen_id}/section/{section_num}")
        return utils.get_json(url)
