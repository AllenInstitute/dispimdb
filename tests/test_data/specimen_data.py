import datetime

specimen_good_data = [
    {
        'specimen_id': '123456',
        'project_id': 'Project1',
        'pedigree': 'mouse',
        'sex': 'F',
        'dob': '2021/04/05',
        'perfusion_date': '2017/04/06',
        'perfusion_age': 5,
        'perfusion_notes': 'Some notes',
        'experiment': 'Imaging',
        'status': 'Stopped',
        'notes': 'More notes'
    },
    {
        'specimen_id': '654321',
        'project_id': 'Project1',
        'pedigree': '',
        'sex': '',
        'dob': '2000/1/1',
        'perfusion_date': '2000/1/1',
        'perfusion_age': 5,
        'perfusion_notes': '',
        'experiment': '',
        'status': '',
        'notes': ''
    }
]

specimen_bad_data = [
    ({}, 404),
    ({}, 404),
    ({}, 404),
    ({}, 404),
    ({}, 404)
]