from datetime import datetime

def generate_acquisition_id(acquisition):
    dt = datetime.fromisoformat(
        acquisition['acquisition_time_utc'])
    dt_string = dt.strftime('%Y%m%dT%H%M%S%fZ')
    return "_".join(map(str, (
        acquisition['specimen_id'],
        acquisition['section_num'],
        acquisition['session_id'],
        dt_string
    )))

acq_good_doc = [
    {
        'section_num': 5,
        'session_id': '091721',
        'specimen_id': '123456',
        'scope': 'ispim2',
        'acquisition_metadata': {},
        'acquisition_time_utc': datetime.utcnow().isoformat(),
        'data_location': {
            'tiff_directory': {
                'name': 'my_dir',
                'status': 'STARTED',
            }
        }
    },
    {
        'section_num': 5,
        'session_id': '091721',
        'specimen_id': '123456',
        'scope': 'ispim2',
        'acquisition_metadata': {},
        'acquisition_time_utc': datetime.utcnow().isoformat(),
        'data_location': {
            'tiff_directory': {
                'name': 'H17_B4_S3_16x_0.5xPBS_overview_25um_step_size_1000um_delta_y',
                'status': 'STARTED'
            }
        },
    },
    {
        'section_num': 6,
        'session_id': '091721',
        'specimen_id': '123456',
        'scope': 'ispim2',
        'acquisition_metadata': {},
        'acquisition_time_utc': datetime.utcnow().isoformat(),
        'data_location': {
            'tiff_directory': {
                'name': 'tiff2',
                'status': 'STARTED'
            }
        }
    }
]

for acquisition in acq_good_doc:
    acquisition['acquisition_id'] = generate_acquisition_id(acquisition)

acq_bad_doc = [
    ({}, 404),
    ({}, 404),
    ({}, 404),
    ({}, 404),
    ({}, 404)
]

acq_good_state_transitions = [
    ['STARTED', 'IN_PROGRESS'],
    ['IN_PROGRESS', 'COMPLETED'],
    ['STARTED', 'ERROR']
]
acq_bad_state_transitions = [
    ['STARTED', 'COMPLETED'],
    ['COMPLETED', 'IN_PROGRESS']
]

acq_good_query = []
acq_bad_query = []