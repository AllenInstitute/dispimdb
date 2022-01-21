import datetime
import json
import math
import os
import subprocess

from flask import (
    Blueprint,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for
)
from werkzeug.exceptions import abort
from PIL import Image

from app.auth import login_required
from app.db import get_db, query_mongo

from . import bp, project, section, specimen

default_session = {
    "session_id": "",
    "specimen_id": "",
    "section_ids": 0,
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

@bp.route("/new_session", methods=("GET", "POST"))
@bp.route("/<specimen_id>/new_session", methods=("GET", "POST"))
@bp.route("/<specimen_id>/session/<session_id>/update", methods=("GET", "POST"))
def session_update(specimen_id=None, session_id=None):
    db = get_db()
    sessions = db.sessions
    specimens = db.specimens
    session_configs = db.session_configs

    dropdown_dict = {}
    dropdown_dict["scope"] = specimens.distinct("scope")
    dropdown_dict["objective"] = specimens.distinct("objective")
    dropdown_dict["objective_angle"] = specimens.distinct("objective_angle")
    dropdown_dict["imaging_bath"] = specimens.distinct("imaging_bath")
    dropdown_dict["laser_power"] = specimens.distinct("laser_power")

    dropdown_dict["session_config"] = session_configs.distinct("config_id")
    session_config_list = []
    for config in session_configs.find({}):
        config.pop("_id")
        session_config_list.append(config)
    
    print(session_config_list)

    specimens_dict = specimens.find({})
    specimen_ids = []
    for specimen in specimens_dict:
        specimen_ids.append(specimen["specimen_id"])
    
    if session_id is not None:
        session_dict = sessions.find_one({
            "session_id": session_id
        })
    else:
        session_dict = default_session.copy()
    
    if specimen_id is not None:
        session_dict["specimen_id"] = specimen_id
    
    if "duplicate" in request.args:
        session_dict["session_id"] = ""
    
    if request.method == "POST":
        error = ""

        if session_dict["session_id"] == "" and \
            sessions.find({"session_id": request.form["session_id"]}).count() > 0:
            error += "session_id already exists, must be unique. \n"
        
        if len(error) > 0:
            flash(error)
        else:
            session_dict["session_id"] = request.form["session_id"]
            session_dict["specimen_id"] = request.form["specimen_id"]
            session_dict["section_ids"] = request.form["section_ids"]
            session_dict["imaging_date"] = request.form["imaging_date"]
            session_dict["scope"] = request.form["scope"]
            session_dict["objective"] = request.form["objective"]
            session_dict["objective_angle"] = request.form["objective_angle"]
            session_dict["imaging_bath"] = request.form["imaging_bath"]
            session_dict["laser_power"] = request.form["laser_power"]
            session_dict["raw_tiff_path"] = request.form["raw_tiff_path"]
            session_dict["gif_path"] = request.form["gif_path"]
            session_dict["notes"] = request.form["notes"]
            if request.form["session_config_select"].startswith("new_"):
                session_dict["session_config"] = request.form["session_config_input"]
                result = session_configs.insert_one({
                    "config_id": request.form["session_config_input"],
                    "magnification_factor": request.form["magnification_factor"],
                    "pixel_size": request.form["pixel_size"],
                    "stage_angle": request.form["stage_angle"]
                })
            else:
                session_dict["session_config"] = request.form["session_config_select"]

            session_dict["last_modified_by"] = g.user
            session_dict["last_modified"] = datetime.datetime.now()

            if session_id is None:
                session_dict["added_by"] = g.user
                session_dict["date_added"] = datetime.datetime.now()
                result = sessions.insert_one(session_dict)
            else:
                result = sessions.update_one({
                    "session_id": session_id },
                    { "$set": session_dict})
            
            print(result)

            image_path = os.path.join(current_app.config['IMAGE_UPLOAD_PATH'],
                request.form["specimen_id"],
                request.form["session_id"])

            try:
                os.makedirs(image_path)
            except OSError:
                pass

            for uploaded_image in request.files.getlist("image_files"):
                outpath = os.path.join(image_path, uploaded_image.filename)
                if uploaded_image.filename != "":
                    try:
                        print(outpath)
                        Image.open(uploaded_image).save(outpath)
                    except OSError:
                        print("cannot create ", uploaded_image)

            return redirect(url_for("tracker.specimen_view",
                                    specimen_id=session_dict["specimen_id"]))

    return render_template("session/update.html",
        session_dict=session_dict,
        specimen_ids=specimen_ids,
        dropdown_dict=dropdown_dict,
        session_config_list=session_config_list)

@bp.route("/<specimen_id>/session/<session_id>/delete", methods=("GET", "POST"))
@login_required
def session_delete(specimen_id=None, session_id=None):
    db = get_db()
    sessions = db.sessions

    session_dict = sessions.find_one({
        "specimen_id": specimen_id,
        "session_id": session_id
    })

    result = sessions.delete_one({
        "specimen_id": specimen_id,
        "session_id": session_id
    })
    print(result)

    return redirect(url_for("tracker.specimen_view",
                            specimen_id=session_dict["specimen_id"]))

@bp.route("/session", methods=("GET", "POST"))
@bp.route("/session/overview", methods=("GET", "POST"))
def session_overview():
    db = get_db()
    sessions = db.sessions

    session_list = query_session(sessions)
    
    print(session_list)
    return render_template("session/overview.html",
        session_list=session_list)

@bp.route("/<specimen_id>/session/<session_id>", methods=("GET", "POST"))
def session_view(specimen_id=None, session_id=None):
    db = get_db()
    sessions = db.sessions
    specimens = db.specimens

    session_dict = sessions.find_one({
        "specimen_id": specimen_id,
        "session_id": session_id
    })

    specimen_dict = specimens.find_one({
        "specimen_id": session_dict["specimen_id"]
    })
    project_id = specimen_dict["project_id"]

    thumbnail_dir = os.path.join("/images",
        session_dict["specimen_id"],
        session_dict["session_id"],
        "thumb_gif")
    
    thumbnail_fn = '/home/samk' + thumbnail_dir
    
    try:
        thumbnail_fn = os.listdir('/home/samk' + thumbnail_dir)[0]
        thumbnail_path = thumbnail_dir + "/" + thumbnail_fn
    except:
        thumbnail_path = ''
        
    return render_template("session/view.html",
        session_dict=session_dict,
        thumbnail_path=thumbnail_path,
        project_id=project_id)

def session_table(specimen_id=None):
    db = get_db()
    sessions = db.sessions
    
    session_list = query_session(sessions,
            specimen_id=specimen_id)

    return session_list

def query_session(collection, specimen_id=None):
    query_dict = {}

    if specimen_id is not None:
        query_dict["specimen_id"] = specimen_id
    
    document_list = query_mongo(collection,
        query_dict=query_dict)
    
    return document_list