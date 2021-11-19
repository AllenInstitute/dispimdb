import os
import pymongo

DATABASE_URI = os.environ.get(
    "DISPIMDB_MONGO_URI",
    'mongodb://localhost:27017')
client = pymongo.MongoClient(DATABASE_URI)
DATABASE_NAME = os.environ.get(
    "DISPIMDB_DATABASE_NAME",
    "test_dispimdb")
dispimdb = client[DATABASE_NAME]
specimens_collection = dispimdb.specimens

def specimen_helper(specimen) -> dict:
    return {
        'specimen_id': specimen['specimen_id'],
        'project_id': specimen['project_id'],
        'pedigree': specimen['pedigree'],
        'sex': specimen['sex'],
        'dob': specimen['dob'],
        'perfusion_date': specimen['perfusion_date'],
        'perfusion_age': specimen['perfusion_age'],
        'perfusion_notes': specimen['perfusion_notes'],
        'experiment': specimen['experiment'],
        'status': specimen['status'],
        'notes': specimen['notes']
    }

def query_specimens():
    specimens = []

    for specimen in specimens_collection.find():
        specimens.append(specimen_helper(specimen))
    
    return specimens

def insert_specimen(specimen_data: dict) -> dict:
    specimen = specimens_collection.insert_one(specimen_data)
    new_specimen = specimens_collection.find_one(
        {'specimen_id': specimen['specimen_id']}
    )
    return specimen_helper(new_specimen)

def query_specimen(specimen_id: str) -> dict:
    specimen = specimens_collection.find_one({'specimen_id': specimen_id})

    if specimen:
        return specimen_helper(specimen)
    else:
        return {}

def update_specimen(specimen_id: str, specimen_data: dict):
    if len(specimen_data) < 1:
        return False
    
    specimen = specimens_collection.find_one({'specimen_id': specimen_id})
    if specimen:
        updated_specimen = specimens_collection.update_one(
            {'specimen_id': specimen_id},
            {'$set': specimen_data}
        )
        if updated_specimen:
            return True
        return False
    return False

def delete_specimen(specimen_id: str):
    specimen = specimens_collection.find_one({'specimen_id': specimen_id})
    
    if specimen:
        specimens_collection.delete_one(
            {'specimen_id': specimen_id}
        )
        return True