import os
import posixpath
import requests

from ddbclient.settings import default_client
from ddbclient.utils import put_json, patch_json, post_json


def put_data_location(base_url, acquisition_id,
                      location_key, data_location_dict):
    acquisition_url = posixpath.join(
        base_url,
        "acquisitions/{}/data_location/{}".format(
            acquisition_id, location_key))
    j = put_json(acquisition_url, json=data_location_dict)
    return j


def update_data_location_state(base_url, acquisition_id, location_key, state):
    acquisition_url = posixpath.join(
        base_url,
        "acquisitions/{}/data_location/{}/status/{}".format(
            acquisition_id, location_key, state))
    j = patch_json(acquisition_url)
    return j


def insert_acquisition(base_url, acquisition_dict):
    acquisition_url = posixpath.join(
        base_url, "new_acquisition")
    j = post_json(acquisition_url, json=acquisition_dict)
    return j


class Acquisition:
    """A class for representing Acquisition objects in DispimDb

    ...

    Attributes
    ----------
    client : dict
        configuration information for connecting to the api
    base_url : str
        url of the server hosting the api
    data : dict
        dict representation of the acquisition metadata

    Methods
    -------
    insert_to_db()
        Insert acquisition object data into DispimDb
    update_in_db()
        Update already-existing acquisition object data in DispimDb
    get_from_db(specimen_id, acquisition_id)
        Get acquistion data from DispimDb
    delete_from_db()
        Delete acquisition object in DispimDb
    get_overview()
        Get overview image of acquisition object as defined in data
    list_contents()
        List contents of acquisition directory as defined in data

    """

    def __init__(self, config=default_client, data=None):
        """
        Parameters
        ----------
        client : dict
            configuration information for connecting to the api
            (Default is config defined in settings.py)
        data : dict
            dict representation of the acquisition metadata

        """

        self.client = config
        self.base_url = os.path.join(self.client['hostname'], self.client['subpath'])

        if data is None:
            self.data = {}
        else:
            self.data = data.copy()

    def insert_to_db(self):
        """Insert data into new document in DispimDb

        Throws error if no data available
        """

        acquisition_url = os.path.join(self.base_url,
            'new_acquisition').replace('\\', '/')

        if self.data:
            r = requests.post(acquisition_url, json=self.data)
            return r.json()
        else:
            # Should raise error
            return 'No data to save'

    def update_in_db(self):
        """Update data of specified document in DispimDb

        Throws error if no data available
        """
        acquisition_url = os.path.join(self.base_url,
            self.data['specimen_id'],
            'acquisition',
            self.data['acquisition_id']).replace('\\', '/')

        r = requests.put(acquisition_url, json=self.data)
        acquisition = r.json()

        return acquisition

    def get_from_db(self, specimen_id, acquisition_id):
        """Update data of specified document in DispimDb

        Parameters
        ----------
        specimen_id : str
            The specimen_id as defined in the acquisition model
        acquisition_id : str
            The acquisition_id as defined in the acquisition model
        """

        if not(isinstance(specimen_id, str)):
            specimen_id = str(specimen_id)

        acquisition_url = os.path.join(self.base_url,
            specimen_id,
            'acquisition',
            acquisition_id).replace('\\', '/')

        r = requests.get(acquisition_url)
        acquisition = r.json()
        self.data.update(acquisition)

        return acquisition

    def delete_from_db(self):
        """Deletes specified acquisition from DispimDb

        Throws error if no data available
        """
        acquisition_url = os.path.join(self.base_url,
            self.data['specimen_id'],
            'acquisition',
            self.data['acquisition_id']).replace('\\', '/')

        r = requests.delete(acquisition_url, json=self.data)
        acquisition = r.json()

        return acquisition

    def get_overview(self):
        """Grabs overview of specified acquisition from
        location specified in DispimDb

        Throws error if no data available
        """
        acquisition_url = os.path.join(self.base_url,
            self.data['specimen_id'],
            'acquisition',
            self.data['acquisition_id'],
            'get_overview').replace('\\', '/')

        r = requests.get(acquisition_url)

        return r

    def list_contents(self):
        """Lists directory contents of specified acquisition from
        location specified in DispimDb

        Throws error if no data available
        """
        acquisition_url = os.path.join(self.base_url,
            self.data['specimen_id'],
            'acquisition',
            self.data['acquisition_id'],
            'list_contents').replace('\\', '/')

        r = requests.get(acquisition_url)
        contents = r.json()

        return contents
