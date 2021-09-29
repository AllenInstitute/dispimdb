import os
import requests

from ddbclient.settings import default_client

class Session:
    def __init__(self, config=default_client, data=None):
        self.client = config
        self.base_url = os.path.join(self.client['hostname'], self.client['subpath'])

        if data is None:
            self.data = {}
        else:
            self.data = data.copy()

    def insert_to_db(self):
        session_url = os.path.join(self.base_url,
            'new_session').replace('\\', '/')
        
        if self.data:
            r = requests.post(session_url, json=self.data)
            return r
        else:
            return 'No data to save'
    
    def update_in_db(self):
        session_url = os.path.join(self.base_url,
            self.data['specimen_id'],
            'session',
            self.data['session_id']).replace('\\', '/')
        
        r = requests.put(session_url, json=self.data)
        session = r.json()
        
        return session
    
    def get_from_db(self, specimen_id, session_id):
        if not(isinstance(specimen_id, str)):
            specimen_id = str(specimen_id)

        session_url = os.path.join(self.base_url,
            specimen_id,
            'session',
            session_id).replace('\\', '/')

        r = requests.get(session_url)
        session = r.json()
        self.data.update(session)

        return session
    
    def delete_from_db(self):
        session_url = os.path.join(self.base_url,
            self.data['specimen_id'],
            'session',
            self.data['session_id']).replace('\\', '/')
        
        r = requests.delete(session_url, json=self.data)
        session = r.json()
        
        return session
            
    def get_acquisitions(self):
        r = requests.get(self.base_url)