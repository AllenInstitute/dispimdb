import os
import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.app.app import app

client = TestClient(app)

def test_create_specimen(mongo_delete_specimens, good_specimens):
    for specimen in good_specimens:
        response = client.post('api/', json=specimen)
        specimen_data = response.json()

        assert response.status_code == 201
        assert specimen_data['specimen_id'] == specimen['specimen_id']

def test_get_specimen(mongo_insert_specimens, good_specimens):
    for specimen in good_specimens:
        response = client.get('api/' + specimen['specimen_id'])
        specimen_data = response.json()

        assert response.status_code == 200
        assert specimen_data['specimen_id'] == specimen['specimen_id']
    
def test_update_specimen(mongo_insert_specimens, good_specimens):
    updated_status = 'Finished'
    for specimen in good_specimens:
        if '_id' in specimen:
            specimen.pop('_id')
        
        specimen['status'] = updated_status
        response = client.put('api/' + specimen['specimen_id'], json=specimen)
        specimen_data = response.json()
        
        assert response.status_code == 202
        assert specimen_data['specimen_id'] == specimen['specimen_id']
        assert specimen_data['status'] == specimen['status']
    
def test_delete_specimen(mongo_insert_specimens, good_specimens):
    for specimen in good_specimens:
        delete_response = client.delete('api/' + specimen['specimen_id'])
        get_response = client.get('api/' + specimen['specimen_id'])

        assert delete_response.status_code == 204
        assert get_response.status_code == 404

def test_create_acquisition(mongo_delete_acquisitions, good_acquisitions):
    for acquisition in good_acquisitions:
        acquisition_url = os.path.join('api/', 'new_acquisition')
        
        response = client.post(acquisition_url, json=acquisition)
        acquisition_data = response.json()

        assert response.status_code == 201
        assert acquisition_data['specimen_id'] == acquisition['specimen_id']
        assert acquisition_data['acquisition_id'] == acquisition['acquisition_id']

def test_get_acquisition(mongo_insert_acquisitions, good_acquisitions):    
    for acquisition in good_acquisitions:
        acquisition_url = os.path.join('api/',
            acquisition['specimen_id'],
            'acquisition',
            acquisition['acquisition_id'])
        
        response = client.get(acquisition_url)
        acquisition_data = response.json()

        assert response.status_code == 200
        assert acquisition_data['specimen_id'] == acquisition['specimen_id']
        assert acquisition_data['acquisition_id'] == acquisition['acquisition_id']

def test_update_acquisition(mongo_insert_acquisitions, good_acquisitions):
    n5_directory = 'my_n5_dir'

    for acquisition in good_acquisitions:
        if '_id' in acquisition:
            acquisition.pop('_id')
        
        acquisition['data_location']['n5_directory'] = n5_directory

        acquisition_url = os.path.join('api/',
            acquisition['specimen_id'],
            'acquisition',
            acquisition['acquisition_id'])
        
        response = client.put(acquisition_url, json=acquisition)
        acquisition_data = response.json()
        
        assert response.status_code == 202
        assert acquisition_data['specimen_id'] == acquisition['specimen_id']
        assert acquisition_data['acquisition_id'] == acquisition['acquisition_id']
        assert acquisition_data['data_location']['n5_directory'] == n5_directory

def test_delete_acquisition(mongo_insert_acquisitions, good_acquisitions):
    for acquisition in good_acquisitions:
        acquisition_url = os.path.join('api/',
            acquisition['specimen_id'],
            'acquisition',
            acquisition['acquisition_id'])
        
        delete_response = client.delete(acquisition_url)
        get_response = client.get(acquisition_url)

        assert delete_response.status_code == 204
        assert get_response.status_code == 404

def test_create_section(mongo_delete_sections, good_sections):
    for section in good_sections:
        section_url = os.path.join('api/', 'new_section')
        
        response = client.post(section_url, json=section)
        section_data = response.json()

        print(section_data)

        assert response.status_code == 201
        assert section_data['specimen_id'] == section['specimen_id']
        assert section_data['section_num'] == section['section_num']

def test_get_section(mongo_insert_sections, good_sections):    
    for section in good_sections:
        section_url = os.path.join('api/',
            section['specimen_id'],
            'section',
            str(section['section_num']))
        
        print(section_url)
        
        response = client.get(section_url)
        section_data = response.json()

        print(section_data)
        print(response.status_code)

        assert response.status_code == 200
        assert section_data['specimen_id'] == section['specimen_id']
        assert section_data['section_num'] == section['section_num']

def test_update_section(mongo_insert_sections, good_sections):
    other_notes = 'Some notes'

    for section in good_sections:
        if '_id' in section:
            section.pop('_id')
        
        section['other_notes'] = other_notes

        section_url = os.path.join('api/',
            section['specimen_id'],
            'section',
            str(section['section_num']))
        
        response = client.put(section_url, json=section)
        section_data = response.json()
        
        assert response.status_code == 202
        assert section_data['specimen_id'] == section['specimen_id']
        assert section_data['section_num'] == section['section_num']
        assert section_data['other_notes'] == other_notes

def test_delete_section(mongo_insert_sections, good_sections):
    for section in good_sections:
        section_url = os.path.join('api/',
            section['specimen_id'],
            'section',
            str(section['section_num']))

        delete_response = client.delete(section_url)
        get_response = client.get(section_url)

        assert delete_response.status_code == 204
        assert get_response.status_code == 404

def test_create_session(mongo_delete_sessions, good_sessions):
    for session in good_sessions:
        session_url = os.path.join('api/', 'new_session')
        
        response = client.post(session_url, json=session)
        session_data = response.json()

        assert response.status_code == 201
        assert session_data['specimen_id'] == session['specimen_id']
        assert session_data['session_id'] == session['session_id']

def test_get_session(mongo_insert_sessions, good_sessions):    
    for session in good_sessions:
        session_url = os.path.join('api/',
            session['specimen_id'],
            'session',
            session['session_id'])
        
        response = client.get(session_url)
        session_data = response.json()

        assert response.status_code == 200
        assert session_data['specimen_id'] == session['specimen_id']
        assert session_data['session_id'] == session['session_id']

def test_update_session(mongo_insert_sessions, good_sessions):
    scope = 'ispim2'

    for session in good_sessions:
        if '_id' in session:
            session.pop('_id')
        
        session['scope'] = scope

        session_url = os.path.join('api/',
            session['specimen_id'],
            'session',
            session['session_id'])
        
        response = client.put(session_url, json=session)
        session_data = response.json()
        
        assert response.status_code == 202
        assert session_data['specimen_id'] == session['specimen_id']
        assert session_data['session_id'] == session['session_id']
        assert session_data['scope'] == scope

def test_delete_session(mongo_insert_sessions, good_sessions):
    for session in good_sessions:
        session_url = os.path.join('api/',
            session['specimen_id'],
            'session',
            session['session_id'])

        delete_response = client.delete(session_url)
        get_response = client.get(session_url)

        assert delete_response.status_code == 204
        assert get_response.status_code == 404