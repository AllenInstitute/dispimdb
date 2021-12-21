import requests

# common utilities for handling requests
#   TODO add retries and exception handling

def post_json(url, data):
    r = requests.post(url, json=data)
    r.raise_for_status()
    return r.json()

def get_json(url, query):
    r = requests.get(url, query)
    r.raise_for_status()
    return r.json()

def put_json(url, query, data):
    r = requests.put(query, json=data)
    return r.json()

def patch_json(url, query, data):
    r = requests.patch(url, query, json=data)
    r.raise_for_status()
    return r.json()

def delete_json(url, query):
    r = requests.delete(url, query)
    r.raise_for_status()
    return r.json()