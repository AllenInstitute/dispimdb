import datetime
import json
import math

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db, query_mongo
from app.forms import ProjectForm
from dispimdb import dispimdb

from . import bp, session, section, specimen

def fill_data_config(data_config):
    for field in data_config:
        print(field)
    
    #return data_config

default_project = {
    "project_id": "",
    "lab_lead": "",
    "description": "",
    "notes": "",
    "added_by": "",
    "date_added": datetime.datetime.min,
    "last_modified_by": "",
    "last_modified": datetime.datetime.min
}

project_data_config = {
    "collection": "project",
    "parents": [],
    "children": ["specimen"],
    "viz_tools": [],
    "data_fields" : {
        "project_id": {
            "display_name": "Project ID",
            "type": "string",
            "field_type": "id_input",
            "required": True,
            "editable": False,
            "hidden": False,
            "overview_viewable": True,
            "table_viewable": True
        },
        "lab_lead": {
            "display_name": "Lab Lead",
            "type": "string",
            "field_type": "select",
            "required": True,
            "editable": True,
            "hidden": False,
            "overview_viewable": True,
            "table_viewable": True
        },
        "description": {
            "display_name": "Description",
            "type": "string",
            "field_type": "textarea",
            "required": False,
            "editable": True,
            "hidden": False,
            "overview_viewable": True,
            "table_viewable": True
        },
        "notes": {
            "display_name": "Notes",
            "type": "string",
            "field_type": "textarea",
            "required": False,
            "editable": True,
            "hidden": False,
            "overview_viewable": True,
            "table_viewable": True
        }
    }
}

project_table_config = {

}

class ProjectCollection(dispimdb.DispimDbCollection):
    def __init__(self):
        pass

class Project:
    def __init__(self, project_dict=default_project):
        self.form = ProjectForm()
        self.project_id = project_dict["project_id"]
        self.lab_lead = project_dict["lab_lead"]
        self.description = project_dict["description"]
        self.notes = project_dict["notes"]
    
    def from_json(self):
        pass

    def to_dict(self):
        pass

class ProjectTable:
    def __init__(self):
        pass

class ProjectPage:
    def __init__(self):
        pass

@bp.route("/projects/update", methods=("GET", "POST"))
@bp.route("/projects/<project_id>/update", methods=("GET", "POST"))
@login_required
def project_update(project_id=None):
    db = get_db()
    projects = db.projects
    users = db.users

    users_json = users.find({})
    usernames = []
    for user in users_json:
        usernames.append(user["username"])
    
    form_select_values = {}
    form_select_values["lab_lead"] = usernames
    
    if project_id is not None:
        project_dict = projects.find_one({
            "project_id": project_id
        })
    else:
        project_dict = default_project
    
    if "duplicate" in request.args:
        project_dict["project_id"] = ""
        
    if request.method == "POST":
        error = ""

        if project_dict["project_id"] == "" and \
            projects.find({"project_id": request.form["project_id"]}).count() > 0:
            error += "Project_id already exists, must be unique. \n"
        
        if len(error) > 0:
            flash(error)
        else:
            project_dict["project_id"] = request.form["project_id"]
            project_dict["lab_lead"] = request.form["lab_lead"]
            project_dict["description"] = request.form["description"]
            project_dict["notes"] = request.form["notes"]
            project_dict["last_modified_by"] = g.user
            project_dict["last_modified"] = datetime.datetime.now()

            if project_id is None:
                project_dict["added_by"] = g.user
                project_dict["date_added"] = datetime.datetime.now()
                result = projects.insert_one(project_dict)
            else:
                result = projects.update_one({
                    "project_id": project_id },
                    { "$set": project_dict })
            
            print(result)

            return redirect(url_for("tracker.project_overview"))

    return render_template("update.html",
        collection_name="Project",
        form_values=project_dict,
        form_select_values=form_select_values,
        form_dict=project_data_config)

@bp.route("/project/<project_id>/delete", methods=("GET", "POST"))
@login_required
def project_delete(project_id=None):
    db = get_db()
    projects = db.projects

    result = projects.delete_one({
        "project_id": project_id
    })
    print(result)

    return redirect(url_for("tracker.project_overview"))

#@bp.route("/project", methods=("GET", "POST"))
#@bp.route("/project/overview", methods=("GET", "POST"))
def project_overview():
    db = get_db()
    projects = db.projects

    project_list = query_project(projects)
        
    return render_template("project/overview.html",
        project_list=project_list)

@bp.route("/project/view/<project_id>", methods=("GET", "POST"))
def project_view(project_id=None):
    db = get_db()
    projects = db.projects

    project_dict = projects.find_one({
        "project_id": project_id
    })
    
    specimen_list = specimen.specimen_table(project_id=project_id)
    
    return render_template("project/view.html",
        project_json=project_dict,
        specimen_list=specimen_list)

def query_project(collection, filters=None):
    query_dict = {}

    document_list = query_mongo(collection,
        query_dict=query_dict)
    
    return document_list 