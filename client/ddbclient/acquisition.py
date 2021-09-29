import os
import requests

from ddbclient.settings import default_client

class Acquisition:
    def __init__(self, config=default_client, data=None):
        self.client = config
        self.base_url = os.path.join(self.client['hostname'], self.client['subpath'])

        if data is None:
            self.data = {}
        else:
            self.data = data.copy()

    def insert_to_db(self):
        acquisition_url = os.path.join(self.base_url,
            'new_acquisition').replace('\\', '/')
        
        if self.data:
            r = requests.post(acquisition_url, json=self.data)
            return r.json()
        else:
            return 'No data to save'
    
    def update_in_db(self):
        acquisition_url = os.path.join(self.base_url,
            self.data['specimen_id'],
            'acquisition',
            self.data['acquisition_id']).replace('\\', '/')
        
        r = requests.put(acquisition_url, json=self.data)
        acquisition = r.json()
        
        return acquisition
    
    def get_from_db(self, specimen_id, acquisition_id):
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
        acquisition_url = os.path.join(self.base_url,
            self.data['specimen_id'],
            'acquisition',
            self.data['acquisition_id']).replace('\\', '/')
        
        r = requests.delete(acquisition_url, json=self.data)
        acquisition = r.json()

        return acquisition
    
    def get_overview(self):
        acquisition_url = os.path.join(self.base_url,
            self.data['specimen_id'],
            'acquisition',
            self.data['acquisition_id'],
            'get_overview').replace('\\', '/')
        
        r = requests.get(acquisition_url)

        return r
    
    def list_contents(self):
        acquisition_url = os.path.join(self.base_url,
            self.data['specimen_id'],
            'acquisition',
            self.data['acquisition_id'],
            'list_contents').replace('\\', '/')
        
        r = requests.get(acquisition_url)
        contents = r.json()

        return contents
    
    def get_block(self):
        acquisition_url = os.path.join(self.base_url,
            self.data['specimen_id'],
            'acquisition',
            self.data['acquisition_id']).replace('\\', '/')
    
    def get_segment(self):
        acquisition_url = os.path.join(self.base_url,
            self.data['specimen_id'],
            'acquisition',
            self.data['acquisition_id']).replace('\\', '/')
    
    def get_strip(self):
        acquisition_url = os.path.join(self.base_url,
            self.data['specimen_id'],
            'acquisition',
            self.data['acquisition_id']).replace('\\', '/')