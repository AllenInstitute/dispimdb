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
                'uri': 'file:///path/to/my_dir',
                'status': 'CREATING',
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
                'uri': 'file:///path/to/H17_B4_S3_16x_0.5xPBS_overview_25um_step_size_1000um_delta_y',
                'status': 'CREATING'
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
                'uri': 'file:///path/to/tiff2',
                'status': 'CREATING'
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

acq_good_query = []
acq_bad_query = []
