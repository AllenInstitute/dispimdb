acquisition_good_data = [
    {
        'acquisition_id': 'acq1',
        'section_num': 5,
        'session_id': '091721',
        'specimen_id': '123456',
        'scope': 'ispim2',
        'acquisition_metadata': {},
        'data_location': {
            'tiff_directory': 'my_dir'
        }
    },
    {
        'acquisition_id': 'acq2',
        'section_num': 5,
        'session_id': '091721',
        'specimen_id': '123456',
        'scope': 'ispim2',
        'acquisition_metadata': {},
        'data_location': {
            'tiff_directory': 'H17_B4_S3_16x_0.5xPBS_overview_25um_step_size_1000um_delta_y'
        }
    }
]

acquisition_bad_data = [
    ({}, 404),
    ({}, 404),
    ({}, 404),
    ({}, 404),
    ({}, 404)
]