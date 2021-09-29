import os
import requests

from ddbclient.settings import default_client

class Section:
    def __init__(self, config=default_client, data=None):
        self.client = config
        self.base_url = os.path.join(self.client['hostname'], self.client['subpath'])

        if data is None:
            self.data = {}
        else:
            self.data = data.copy()

    def insert_to_db(self):
        section_url = os.path.join(self.base_url,
            'new_section').replace('\\', '/')
        
        if self.data:
            r = requests.post(section_url, json=self.data)
            return r.json()
        else:
            return 'No data to save'
    
    def update_in_db(self):
        section_url = os.path.join(self.base_url,
            self.data['specimen_id'],
            'section',
            self.data['section_num']).replace('\\', '/')
        
        r = requests.put(section_url, json=self.data)
        section = r.json()
        
        return section
    
    def get_from_db(self, specimen_id, section_num):
        if not(isinstance(specimen_id, str)):
            specimen_id = str(specimen_id)

        section_url = os.path.join(self.base_url,
            specimen_id,
            'section',
            section_num).replace('\\', '/')

        r = requests.get(section_url)
        section = r.json()
        self.data.update(section)

        return section
    
    def delete_from_db(self):
        section_url = os.path.join(self.base_url,
            self.data['specimen_id'],
            'section',
            self.data['section_num']).replace('\\', '/')
        
        r = requests.delete(section_url, json=self.data)
        section = r.json()
        
        return section
            
    def get_sessions(self):
        r = requests.get(self.base_url)