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


def put_json(url, data):
    r = requests.put(url, json=data)
    r.raise_for_status()
    return r.json()


def patch_json(url):
    r = requests.patch(url)
    r.raise_for_status()
    return r.json()


def delete_json(url):
    r = requests.delete(url)
    r.raise_for_status()
    if r.status_code == 204:
        return None
    else:
        return r.json()
