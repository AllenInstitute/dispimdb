import requests
import datetime

def get_specimen():
    specimen_url = "http://bigkahuna.corp.alleninstitute.org/api/574065"

    r = requests.get(specimen_url)
    return r.text

def add_session():
    add_session_url = "http://bigkahuna.corp.alleninstitute.org/api/560105/new_session"
    new_session = {
        "session_id": "071621",
        "specimen_id": "560105",
        "section_ids": 7,
        "imaging_date": "",
        "scope": "",
        "objective": "",
        "objective_angle": "",
        "imaging_bath": "",
        "laser_power": "",
        "session_config": "",
        "raw_tiff_path": "",
        "gif_path": "",
        "notes": "",
        "date_added": "",
        "added_by": "",
        "last_modified": "",
        "last_modified_by": ""
    }

    r = requests.post(add_session_url, json=new_session)
    return r.text

def run_job():
    run_job_url = "http://bigkahuna.corp.alleninstitute.org/api/ijm_test/541177/session/20210716"
    r = requests.post(run_job_url)

    return r.text

def get_job_status():
    status_url = "http://bigkahuna.corp.alleninstitute.org/api/ijm_test/541177/session/20210716/status"
    r = requests.get(status_url)

    return r.text