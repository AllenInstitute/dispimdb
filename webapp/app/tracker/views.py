import datetime
import json
import math

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for
)

from app.auth import login_required
from app.db import get_db, query_mongo

from . import bp
from .collections import collections

default_config_data = {
    "display_name": "no_name",
    "type": "string",
    "field_type": "input",
    "required": False,
    "editable": True,
    "overview_viewable": True,
    "table_viewable": True
}

timestamp_config = {
    "added_by": {
        "display_name": "Added By",
        "type": "string",
        "field_type": "hidden",
        "required": True,
        "editable": False,
        "overview_viewable": False,
        "table_viewable": True
    },
    "date_added": {
        "display_name": "Date Added",
        "type": "string",
        "field_type": "hidden",
        "required": True,
        "editable": False,
        "overview_viewable": True,
        "table_viewable": True
    },
    "last_modified_by": {
        "display_name": "Last Modified By",
        "type": "string",
        "field_type": "hidden",
        "required": True,
        "editable": False,
        "overview_viewable": False,
        "table_viewable": True
    },
    "last_modified": {
        "display_name": "Last Modified",
        "type": "string",
        "field_type": "hidden",
        "required": True,
        "editable": False,
        "overview_viewable": True,
        "table_viewable": True
    }
}

@bp.route('/update')
def update():
    pass

@bp.route('/delete')
def delete():
    pass

@bp.route('/<collection_name>/<collection_id>/view')
def view(collection_name, collection_id):
    db = get_db()
    collection = db[collection_name]
    collection_data_config = fill_data_config(collections[collection_name])
    identifiers = collection_data_config["identifiers"]

    query = {}
    for identifier in identifiers:
        query[identifier] = collection_id

    document_dict = collection.find_one(query)
    print(document_dict)

    children = collection_data_config["children"]
    print(children)
    #specimen_list = specimen.specimen_table(project_id=project_id)
    children_documents = {}
    for child in children:
        children_documents[child] = table(child, collection_id, collection_name)
    
    print(children_documents)
    
    return render_template("view.html",
        document_dict=document_dict,
        children_documents=children_documents)

@bp.route('/<collection_name>')
@bp.route('/<collection_name>/overview')
def overview(collection_name):
    db = get_db()
    collection = db[collection_name]

    document_list = query_collection(collection)
    collection_data_config = fill_data_config(collections[collection_name])
        
    return render_template("overview.html",
        collection_data_config=collection_data_config,
        document_list=document_list)

def table(collection_name, collection_id, parent):
    db = get_db()
    collection = db[collection_name]

    parent_id = collections[parent]["identifiers"][0]
    
    document_list = query_collection(collection,
            query={parent_id: collection_id})
    
    return document_list

def fill_data_config(data_config):
    for field in data_config["data_fields"]:
        missing = list(set(default_config_data.keys()) - set(data_config["data_fields"][field].keys()))
        for config_field in missing:
            data_config["data_fields"][field][config_field] = default_config_data[config_field]
    
    data_config["data_fields"].update(timestamp_config)
    
    return data_config

def query_collection(collection, query=None):
    document_list = query_mongo(collection,
        query_dict=query)
    
    return document_list
