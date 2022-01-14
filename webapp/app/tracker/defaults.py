import datetime

default_config_data = {
    "display_name": "No Display Name",
    "type": "string",
    "field_type": "input",
    "required": False,
    "editable": True,
    "hidden": False,
    "overview_viewable": True,
    "table_viewable": True
}

default_specimen = {
    "specimen_id": "",
    "project_id": "NA",
    "pedigree": "",
    "sex": "",
    "dob": "",
    "perfusion_date": "",
    "perfusion_age": "",
    "perfusion_notes": "",
    "experiment": "",
    "status": "",
    "notes": "",
    "added_by": "",
    "date_added": datetime.datetime.now(),
    "last_modified_by": "",
    "last_modified": datetime.datetime.now()
}

specimen_form_config = {
    "data_fields": {
        "specimen_id": {
            "display_name": "Specimen ID",
            "field_type": "id_input"
        },
        "project_id": {
            "display_name": "Project ID",
            "field_type": "select"
        },
        "pedigree": {
            "display_name": "Pedigree",
            "field_type": "select_input"
        },
        "sex": {
            "display_name": "Sex",
            "field_type": "select"
        },
        "dob": {
            "display_name": "Date of Birth",
            "field_type": "input_date"
        },
        "perfusion_date": {
            "display_name": "Perfusion Date",
            "field_type": "input_date"
        },
        "perfusion_age": {
            "display_name": "Perfusion Age",
            "field_type": "input"
        },
        "perfusion_notes": {
            "display_name": "Perfusion Notes",
            "field_type": "textarea"
        },
        "experiment": {
            "display_name": "Experiment",
            "field_type": "select_input"
        },
        "status": {
            "display_name": "Status",
            "field_type": "select_input"
        },
        "notes": {
            "display_name": "Notes",
            "field_type": "textarea"
        }
    }
}

specimen_table_config = {

}

default_section = {
    "section_id": "",
    "specimen_id": "",
    "imaging_sessions_ids": [],
    "cut_plane": "",
    "thickness": "",
    "prep_type": "",
    "fluorescent_labels": "",
    "other_notes": "",
    "date_added": datetime.datetime.min,
    "added_by": "",
    "last_modified": datetime.datetime.min,
    "last_modified_by": ""
}

default_session = {
    "session_id": "",
    "specimen_id": "",
    "section_ids": [],
    "imaging_date": datetime.datetime.min,
    "scope": "",
    "objective": "",
    "objective_angle": "",
    "imaging_bath": "",
    "laser_power": "",
    "raw_tiff_path": "",
    "gif_path": "",
    "notes": "",
    "date_added": datetime.datetime.min,
    "added_by": "",
    "last_modified": datetime.datetime.min,
    "last_modified_by": ""
}
