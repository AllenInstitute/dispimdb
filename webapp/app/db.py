import pymongo

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.client = pymongo.MongoClient(
            current_app.config['DATABASE_URI'],
            connect=False
        )
        g.db = g.client[current_app.config['DATABASE_NAME']]
    
    return g.db

def query_mongo(collection, query_dict={}, skip=0, limit=1000, filters=None):
    document_list = []
    
    documents = collection.find(query_dict) \
        .sort('last_modified', pymongo.DESCENDING) \
        .skip(skip) \
        .limit(limit)
    for document in documents:
        document.pop('_id')
        document_list.append(document)
    
    return document_list

def close_db(e=None):
    client = g.pop('client', None)

    if client is not None:
        client.close()

def init_db():
    pass

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

