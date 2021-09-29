project_data_config = {
    "collection": "projects",
    "collection_name": "Projects",
    "identifiers": ["project_id"],
    "parents": [],
    "children": ["specimens"],
    "viz_tools": [],
    "data_fields": {
        "project_id": {
            "display_name": "Project ID",
            "required": True,
            "editable": False,
        },
        "lab_lead": {
            "display_name": "Lab Lead",
            "type": "string",
            "field_type": "select",
            "required": True,
        },
        "description": {
            "display_name": "Description",
            "type": "string",
            "field_type": "textarea",
        },
        "notes": {
            "display_name": "Notes",
            "type": "string",
            "field_type": "textarea",
            "table_viewable": False
        }
    }
}

specimen_data_config = {
    "collection": "specimens",
    "collection_name": "Specimens",
    "identifiers": ["specimen_id"],
    "parents": ["projects"],
    "children": ["sections", "sessions"],
    "viz_tools": [],
    "data_fields": {}
}

collections = {
    "projects": project_data_config,
    "specimens": specimen_data_config
}