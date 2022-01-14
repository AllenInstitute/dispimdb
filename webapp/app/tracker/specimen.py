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

from . import bp, session, project, section
from .defaults import default_specimen, specimen_form_config

@bp.route("/new_specimen", methods=("GET", "POST"))
@bp.route("/<specimen_id>/update", methods=("GET", "POST"))
@bp.route("/<project_id>/new_specimen", methods=("GET", "POST"))
@login_required
def specimen_update(project_id=None, specimen_id=None):
    db = get_db()
    projects = db.projects
    specimens = db.specimens

    dropdown_dict = {}
    dropdown_dict["sex"] = ["Male", "Female"]
    dropdown_dict["pedigree"] = specimens.distinct("pedigree")
    dropdown_dict["experiment"] = specimens.distinct("experiment")
    dropdown_dict["status"] = specimens.distinct("status")

    projects_dict = projects.find({})
    project_ids = []
    for project in projects_dict:
        project_ids.append(project["project_id"])
    
    dropdown_dict["project_id"] = project_ids
    
    if specimen_id is not None:
        specimen_dict = specimens.find_one({
            "specimen_id": specimen_id
        })
    else:
        specimen_dict = default_specimen.copy()
    
    if project_id is not None:
        specimen_dict["project_id"] = project_id
    
    if "duplicate" in request.args:
        specimen_dict["specimen_id"] = ""

    if isinstance(specimen_dict["dob"], datetime.datetime):
        specimen_dict["dob"] = specimen_dict["dob"].strftime("%m/%d/%y")
    
    if isinstance(specimen_dict["perfusion_date"], datetime.datetime):
        specimen_dict["perfusion_date"] = specimen_dict["perfusion_date"].strftime("%m/%d/%y")
    
    if request.method == 'POST':
        error = ""

        if specimen_dict["specimen_id"] == "" and \
            specimens.find({"specimen_id": request.form["specimen_id"]}).count() > 0:
            error += "specimen_id already exists, must be unique. \n"
        
        try:
            if len(request.form["dob"]) > 0:
                dob = datetime.datetime.strptime(request.form["dob"], "%m/%d/%y")
                dob = dob.strftime("%m/%d/%y")
            else:
                dob = ""
        except ValueError:
            error += "Incorrect Date of Birth format, must be mm/dd/yy. \n"

        try:
            if len(request.form["perfusion_date"]) > 0:
                perfusion_date = datetime.datetime.strptime(request.form["perfusion_date"], "%m/%d/%y")
                perfusion_date = perfusion_date.strftime("%m/%d/%y")
            else:
                perfusion_date = ""
        except ValueError:
            error += "Incorrect Perfusion Date format, must be mm/dd/yy. \n"
        
        try:
            if len(request.form["perfusion_age"]) > 0:
                perfusion_age = int(request.form["perfusion_age"])
            else:
                perfusion_age = ""
        except ValueError:
            error += "Perfusion Age must be an integer. \n"
        
        if len(error) > 0:
            flash(error)
        else:
            specimen_dict["specimen_id"] = request.form["specimen_id"]
            specimen_dict["project_id"] = request.form["project_id"]
            if request.form["pedigree_select"].startswith("new_"):
                specimen_dict["pedigree"] = request.form["pedigree_input"]
            else:
                specimen_dict["pedigree"] = request.form["pedigree_select"]
            specimen_dict["sex"] = request.form["sex"]
            specimen_dict["dob"] = dob
            specimen_dict["perfusion_date"] = perfusion_date
            specimen_dict["perfusion_age"] = perfusion_age
            specimen_dict["perfusion_notes"] = request.form["perfusion_notes"]
            if request.form["experiment_select"].startswith("new_"):
                specimen_dict["experiment"] = request.form["experiment_input"]
            else:
                specimen_dict["experiment"] = request.form["experiment_select"]
            if request.form["status_select"].startswith("new_"):
                specimen_dict["status"] = request.form["status_input"]
            else:
                specimen_dict["status"] = request.form["status_select"]
            specimen_dict["notes"] = request.form["notes"]
            specimen_dict["last_modified_by"] = g.user
            specimen_dict["last_modified"] = datetime.datetime.now()
        
            if specimen_id is None:
                specimen_dict["added_by"] = g.user
                specimen_dict["date_added"] = datetime.datetime.now()
                result = specimens.insert_one(specimen_dict)
            else:
                result = specimens.update_one({
                    "specimen_id": specimen_id },
                    { "$set": specimen_dict })
            
            print(result)

            return redirect(url_for("tracker.project_view",
                project_id=specimen_dict["project_id"]))
    
    return render_template("update.html",
        collection_name="Specimen",
        form_values=specimen_dict,
        form_select_values=dropdown_dict,
        form_dict=specimen_form_config)

@bp.route("/<specimen_id>/delete", methods=("GET", "POST"))
@login_required
def specimen_delete(specimen_id=None):
    db = get_db()
    specimens = db.specimens
    
    specimen_dict = specimens.find_one({
        "specimen_id": specimen_id
    })

    result = specimens.delete_one({
        "specimen_id": specimen_id
    })
    print(result)

    return redirect(url_for("tracker.project_view",
                            project_id=specimen_dict["project_id"]))

@bp.route("/overview", methods=("GET", "POST"))
def specimen_overview():
    specimen_list = specimen_table()
    
    return render_template("specimen/overview.html",
        specimen_list=specimen_list)

@bp.route("/<specimen_id>", methods=("GET", "POST"))
def specimen_view(specimen_id=None):
    db = get_db()
    specimens = db.specimens

    specimen_dict = specimens.find_one({
        "specimen_id": specimen_id
    })

    section_list = section.section_table(specimen_id=specimen_id)
    session_list = session.session_table(specimen_id=specimen_id)
    
    return render_template("specimen/view.html",
        specimen_dict=specimen_dict,
        section_list=section_list,
        session_list=session_list)

def specimen_table(project_id=None):
    db = get_db()
    specimens = db.specimens
    
    specimen_list = query_specimen(specimens,
            project_id=project_id)
    
    return specimen_list

def query_specimen(collection, project_id=None, filters=None):
    query_dict = {}

    if project_id is not None:
        query_dict["project_id"] = project_id
    
    document_list = query_mongo(collection,
        query_dict=query_dict)
    
    return document_list