from dataclasses import dataclass
from datetime import datetime
import os
import requests

from ddbclient.settings import default_client
from ddbclient import utils

client = default_client

@dataclass
class Acquisition:
    section_num: int
    session_id: str
    specimen_id: str
    scope: str
    acquisition_time_utc: datetime

    acquisition_id: str = ""
    acquisition_metadata: dict = {}
    data_location: dict = {}

def post(data):
    url = os.path.join([client.hostname,
        client.subpath,
        'new_acquisition'])

    response = utils.post_json(url, data)
    return response

def get(acquisition_id):
    url = os.path.join([client.hostname,
        client.subpath,
        'acquisition',
        acquisition_id])

    query = {'acquisition_id': acquisition_id}

    response = utils.get_json(url, query)
    return response

def query(query):
    url = os.path.join([client.hostname,
        client.subpath,
        'acquisition',
        'query'])

def put(acquisition_id, data):
    url = os.path.join([client.hostname,
        client.subpath,
        'acquisition',
        acquisition_id])
    
    query = {'acquisition_id': acquisition_id}

    response = utils.put_json(url, query, data)
    return response

def patch(acquisition_id, data):
    url = os.path.join([client.hostname,
        client.subpath,
        'acquisition',
        acquisition_id])
    
    query = {'acquisition_id': acquisition_id}

    response = utils.patch_json(url, query, data)
    return response

def patch_status(acquisition_id, status):
    pass

def delete(acquisition_id):
    url = os.path.join([client.hostname,
        client.subpath,
        'acquisition',
        acquisition_id])
    
    query = {'acquisition_id': acquisition_id}

    response = utils.delete_json(url, query)
    return response