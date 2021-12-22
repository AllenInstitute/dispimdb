from dataclasses import dataclass
from datetime import datetime
import os
import requests

from ddbclient.settings import default_client
from ddbclient import utils

client = default_client

def post(data):
    url = os.path.join(client['hostname'],
        client['subpath'],
        'new_acquisition')

    response_json = utils.post_json(url, data)

    return response_json['acquisition_id']

def get_all(specimen_id):
    url = os.path.join(client['hostname'],
        client['subpath'],
        specimen_id,
        'acquisitions')
    
    query = {'specimen_id': specimen_id}

    response = utils.get_json(url, query)
    return response

def get(acquisition_id):
    url = os.path.join(client['hostname'],
        client['subpath'],
        'acquisition',
        acquisition_id)

    query = {'acquisition_id': acquisition_id}

    response_json = utils.get_json(url, query)
    return response_json

def query(query):
    url = os.path.join(client['hostname'],
        client['subpath'],
        'acquisition',
        'query')
    
    response = utils.get_json(url, query)
    return response

'''
def put(acquisition_id, data):
    url = os.path.join(client.hostname,
        client.subpath,
        'acquisition',
        acquisition_id)
    
    query = {'acquisition_id': acquisition_id}

    response = utils.put_json(url, query, data)
    return response

def patch(acquisition_id, data):
    url = os.path.join(client.hostname,
        client.subpath,
        'acquisition',
        acquisition_id)
    
    query = {'acquisition_id': acquisition_id}

    response = utils.patch_json(url, query, data)
    return response
'''

def put_data_location(acquisition_id, data_key, data_location):
    url = os.path.join(client['hostname'],
        client['subpath'],
        'acquisition',
        acquisition_id,
        'data_location',
        data_key)
        
    response_json = utils.put_json(url, data_location)
    return response_json

def patch_status(acquisition_id, data_key, state):
    url = os.path.join(client['hostname'],
        client['subpath'],
        'acquisition',
        acquisition_id,
        'data_location',
        data_key,
        'status',
        state)
        
    response_json = utils.patch_json(url)
    return response_json

def delete(acquisition_id):
    url = os.path.join(client['hostname'],
        client['subpath'],
        'acquisition',
        acquisition_id)
    
    response_json = utils.delete_json(url)
    return response_json