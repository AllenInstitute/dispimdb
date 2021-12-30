from dataclasses import dataclass
from datetime import datetime
import os
import requests

from ddbclient import utils

class AcquisitionClient:
    def __init__(self,
                 base_url=None,
                 hostname=None,
                 port=None,
                 subpath=None):
        self.base_url = base_url
        self.hostname = hostname
        self.port = port
        self.subpath = subpath

        if self.port is not None:
            self.hostname = self.hostname + ':' + self.port

        if self.base_url is None:
            self.base_url = os.path.join(
                self.hostname,
                self.subpath
            ).replace('\\', '/')
        else:
            self.base_url = os.path.join(
                self.base_url,
                self.subpath
            ).replace('\\', '/')

    def post(self, data):
        url = os.path.join(self.base_url,
            'new_acquisition')

        response_json = utils.post_json(url, data)

        return response_json['acquisition_id']

    def get_all(self, specimen_id):
        url = os.path.join(self.base_url,
            specimen_id,
            'acquisitions')
        
        query = {'specimen_id': specimen_id}

        response = utils.get_json(url, query)
        return response

    def get(self, acquisition_id):
        url = os.path.join(self.base_url,
            'acquisition',
            acquisition_id)

        query = {'acquisition_id': acquisition_id}

        response_json = utils.get_json(url, query)
        return response_json

    def query(self, query):
        url = os.path.join(self.base_url,
            'acquisition',
            'query')
        
        response_json = utils.get_json(url, query)
        return response_json

    '''
    def put(self, acquisition_id, data):
        url = os.path.join(self.base_url,
            'acquisition',
            acquisition_id)
        
        query = {'acquisition_id': acquisition_id}

        response = utils.put_json(url, query, data)
        return response

    def patch(self, acquisition_id, data):
        url = os.path.join(self.base_url,
            'acquisition',
            acquisition_id)
        
        query = {'acquisition_id': acquisition_id}

        response = utils.patch_json(url, query, data)
        return response
    '''

    def put_data_location(self, acquisition_id, data_key, data_location):
        url = os.path.join(self.base_url,
            'acquisition',
            acquisition_id,
            'data_location',
            data_key)
            
        response_json = utils.put_json(url, data_location)
        return response_json

    def patch_status(self, acquisition_id, data_key, state):
        url = os.path.join(self.base_url,
            'acquisition',
            acquisition_id,
            'data_location',
            data_key,
            'status',
            state)
            
        response_json = utils.patch_json(url)
        return response_json

    def delete(self, acquisition_id):
        url = os.path.join(self.base_url,
            'acquisition',
            acquisition_id)
        
        response_json = utils.delete_json(url)
        return response_json