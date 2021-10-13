section_good_data = [
    {
        'specimen_id': '123456',
        'section_num': 1,
        'cut_plane': 'A string',
        'fluorescent_labels': 'A string',
        'other_notes': 'A string',
        'prep_type': 'A string',
        'thickness': 'A string'
    },
    {
        'specimen_id': '123456',
        'section_num': 2,
        'cut_plane': 'A string',
        'fluorescent_labels': 'A string',
        'other_notes': 'A string',
        'prep_type': 'A string',
        'thickness': 'A string'
    },
    {
        'specimen_id': '654321',
        'section_num': 1,
        'cut_plane': 'A string',
        'fluorescent_labels': 'A string',
        'other_notes': 'A string',
        'prep_type': 'A string',
        'thickness': 'A string'
    }
]

section_bad_data = [
    ({}, 404),
    ({}, 404),
    ({}, 404),
    ({}, 404),
    ({}, 404)
]