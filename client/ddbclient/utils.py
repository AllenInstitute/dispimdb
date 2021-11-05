import requests

# common utilities for handling requests
#   TODO add retries and exception handling


def put_json(*args, **kwargs):
    r = requests.put(*args, **kwargs)
    return r.json()


def patch_json(*args, **kwargs):
    r = requests.patch(*args, **kwargs)
    r.raise_for_status()
    return r.json()


def post_json(*args, **kwargs):
    r = requests.post(*args, **kwargs)
    r.raise_for_status()
    return r.json()
