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

from . import bp, project, session, section, specimen

@bp.route('/', methods=('GET', 'POST'))
def home():
    db = get_db()
    '''
    projects = db.projects
    specimens = db.specimens

    project_list = projects.distinct("project_id")
    print(project_list)

    specimens_cursor = specimens.find({})
    specimen_list = []
    for specimen in specimens_cursor:
        specimen_dict = {}
        specimen_dict["specimen_id"] = specimen["specimen_id"]
        specimen_dict["project_id"] = specimen["project_id"]

        specimen_list.append(specimen_dict)
    
    print(project_list)
    print(specimen_list)
    '''

    #if request.method == "POST":
    #    return redirect(url_for("tracker.project_view", project_id=request.form["projects"]))

    return render_template("tracker.html")

@bp.context_processor
def get_projects():
    db = get_db()
    projects = db.projects

    project_list = projects.distinct("project_id")
    print(project_list)

    print(request)
    if request.method == "POST":
        print(request.form["projects"])
        redirect(url_for("tracker.project_view", project_id=request.form["projects"]))

    return dict(project_list=project_list)
