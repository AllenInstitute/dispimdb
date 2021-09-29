import os
import requests

from ddbclient.settings import default_client

class Specimen:
    def __init__(self, config=default_client, data=None):
        self.client = config
        self.base_url = os.path.join(self.client['hostname'], self.client['subpath'])

        if data is None:
            self.data = {}
        else:
            self.data = data.copy()

    def insert_to_db(self):
        if self.data:
            r = requests.post(self.base_url, json=self.data)
            return r.json()
        else:
            return 'No data to save'
    
    def update_in_db(self):
        specimen_url = os.path.join(self.base_url,
            self.data['specimen_id']).replace('\\', '/')
        
        r = requests.put(specimen_url, json=self.data)
        specimen = r.json()
        
        return specimen
    
    def get_from_db(self, specimen_id):
        if not(isinstance(specimen_id, str)):
            specimen_id = str(specimen_id)

        specimen_url = os.path.join(self.base_url,
            specimen_id).replace('\\', '/')

        r = requests.get(specimen_url)
        specimen = r.json()
        self.data.update(specimen)

        return specimen
    
    def delete_from_db(self):
        specimen_url = os.path.join(self.base_url,
            self.data['specimen_id']).replace('\\', '/')
        
        r = requests.delete(specimen_url, json=self.data)
        specimen = r.json()
        
        return specimen
        
    def get_sections(self):
        sections_url = os.path.join(self.base_url,
            self.data['specimen_id'],
            'sections').replace('\\', '/')
        
        r = requests.get(sections_url)
        sections = r.json()

        return sections
    
    def get_sessions(self):
        sessions_url = os.path.join(self.base_url,
            self.data['specimen_id'],
            'sessions').replace('\\', '/')
        
        r = requests.get(sessions_url)
        sessions = r.json()

        return sessions
    
    def get_acquisitions(self):
        acquisitions_url = os.path.join(self.base_url,
            self.data['specimen_id'],
            'acquisitions').replace('\\', '/')
        
        r = requests.get(acquisitions_url)
        acquisitions = r.json()

        return acquisitions