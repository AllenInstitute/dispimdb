import datetime
import io
import json
import math
import os

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
from . import bp, session, project, specimen

default_section = {
    "section_num": "",
    "specimen_id": "",
    "cut_plane": "",
    "thickness": "",
    "prep_type": "",
    "fluorescent_labels": "",
    "other_notes": "",
    "date_added": "",
    "added_by": "",
    "last_modified": "",
    "last_modified_by": ""
}

@bp.route("/sections/update", methods=("GET", "POST"))
@bp.route("/sections/<specimen_id>/update", methods=("GET", "POST"))
@bp.route("/sections/<specimen_id>/<section_num>/update", methods=("GET", "POST"))
@login_required
def section_update(specimen_id=None, section_num=None):
    db = get_db()
    projects = db.projects
    specimens = db.specimens
    sections = db.sections

    dropdown_dict = {}
    dropdown_dict["cut_plane"] = sections.distinct("cut_plane")
    dropdown_dict["thickness"] = sections.distinct("thickness")
    dropdown_dict["prep_type"] = sections.distinct("prep_type")
    dropdown_dict["fluorescent_labels"] = sections.distinct("fluorescent_labels")

    projects_dict = projects.find({})
    project_ids = []
    for project in projects_dict:
        project_ids.append(project["project_id"])

    specimens_dict = specimens.find({})
    print(specimens_dict)
    specimen_ids = []
    for specimen in specimens_dict:
        specimen_ids.append(specimen["specimen_id"])
    
    if section_num is not None:
        section_dict = sections.find_one({
            "section_num": section_num,
            "specimen_id": specimen_id
        })
    else:
        section_dict = default_section

    if "duplicate" in request.args:
        section_dict["section_num"] = ""
    
    if request.method == "POST":
        error = ""

        if section_dict["section_num"] == "" and \
            sections.find({"specimen_id": request.form["specimen_id"],
                "section_num": request.form["section_num"]}).count() > 0:
            error += "section_num for specimen_id already exists, must be unique. \n"
        
        if len(error) > 0:
            flash(error)
        else:
            section_dict["specimen_id"] = request.form["specimen_id"]
            section_dict["cut_plane"] = request.form["cut_plane"]
            section_dict["thickness"] = request.form["thickness"]
            section_dict["prep_type"] = request.form["prep_type"]
            section_dict["fluorescent_labels"] = request.form["fluorescent_labels"]
            section_dict["other_notes"] = request.form["other_notes"]
            section_dict["last_modified_by"] = g.user
            section_dict["last_modified"] = datetime.datetime.now()

            if section_num is None:
                section_dict["added_by"] = g.user
                section_dict["date_added"] = datetime.datetime.now()
                section_nums_list = parse_section_nums(request.form["section_num"])
                print(section_nums_list)
                for num in section_nums_list:
                    section_dict["section_num"] = str(num)
                    section_dict.pop("_id") if "_id" in section_dict else None
                    print(section_dict)
                    result = sections.insert_one(section_dict)

                    image_path = os.path.join(current_app.config['IMAGE_UPLOAD_PATH'],
                    request.form["specimen_id"],
                    str(num))

                    try:
                        os.makedirs(image_path)
                    except OSError:
                        pass
            else:
                result = sections.update_one({
                    "specimen_id": section_dict["specimen_id"],
                    "section_num": section_num},
                    { "$set": section_dict })
                
                image_path = os.path.join(current_app.config['IMAGE_UPLOAD_PATH'],
                    request.form["specimen_id"],
                    section_num)
                
                for uploaded_image in request.files.getlist("image_files"):
                    outpath = os.path.join(image_path, uploaded_image.filename)
                    if uploaded_image.filename != "":
                        try:
                            print(outpath)
                            Image.open(uploaded_image).save(outpath)
                        except OSError:
                            print("cannot create ", uploaded_image)
            
            print(result)

            return redirect(url_for("tracker.section_overview"))
    
    return render_template("section/update.html",
        section_dict=section_dict,
        specimen_ids=specimen_ids,
        project_ids=project_ids,
        dropdown_dict=dropdown_dict)

@bp.route("/section/delete/<specimen_id>/<section_num>", methods=("GET", "POST"))
@login_required
def section_delete(specimen_id=None, section_num=None):
    db = get_db()
    sections = db.sections

    result = sections.delete_one({
        "specimen_id": specimen_id,
        "section_num": section_num
    })
    print(result)

    return redirect(url_for("tracker.section_overview"))

@bp.route("/section", methods=("GET", "POST"))
@bp.route("/section/overview", methods=("GET", "POST"))
def section_overview():
    db = get_db()
    sections = db.sections

    section_list = query_section(sections)
    
    return render_template("section/overview.html",
        section_list=section_list)

@bp.route("/section/view/<specimen_id>/<section_num>", methods=("GET", "POST"))
def section_view(specimen_id=None, section_num=None):
    db = get_db()
    sections = db.sections

    section_dict = sections.find_one({
        "specimen_id": specimen_id,
        "section_num": section_num
    })

    thumbnail_dir = os.path.join("images",
        section_dict["specimen_id"],
        section_dict["section_num"])
    
    try:
        thumbnail_fn = os.listdir(os.path.join(os.getcwd(),
            "app", "static",
            thumbnail_dir))[0]
        thumbnail_path = os.path.join(thumbnail_dir, thumbnail_fn)
    except:
        thumbnail_path = ""
    
    print(thumbnail_path)
    
    return render_template("section/view.html",
        section_dict=section_dict,
        thumbnail_path=thumbnail_path)

def section_table(specimen_id=None):
    db = get_db()
    sections = db.sections
    
    section_list = query_section(sections,
            specimen_id=specimen_id)

    return section_list

def query_section(collection, specimen_id=None):
    query_dict = {}

    if specimen_id is not None:
        query_dict["specimen_id"] = specimen_id
    
    document_list = query_mongo(collection,
        query_dict=query_dict)
    
    return document_list

def parse_section_nums(nums_string):
    nums_split = nums_string.replace(" ", "").split(",")
    nums_list = []

    for nums in nums_split:
        try:
            nums_dash = nums.split("-")
            if len(nums) > 1 and len(nums_dash) == 2:
                start_num = int(nums_dash[0])
                stop_num = int(nums_dash[1])

                for num in range(start_num, stop_num + 1):
                    nums_list.append(num)
            else:
                nums_list.append(int(nums))
        except ValueError:
            pass

    return nums_list