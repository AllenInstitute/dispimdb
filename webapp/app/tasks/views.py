import os
import subprocess
import sys

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for
)

from app.db import get_db
from . import bp

@bp.route("/<specimen_id>/<section_num>/<session_id>/generate_gif", methods=("GET", "POST"))
def generate_gif(specimen_id, section_num, session_id):
    db = get_db()
    sections = db.sections
    sessions = db.sessions

    section_dict = sections.find_one({
        "section_num": section_num,
        "specimen_id": specimen_id
    })

    session_dict = sessions.find_one({
        "session_id": session_id
    })

    if request.method == "POST":
        if request.form["submit"] == "add":
            print("I'm adding!")
            add.delay(int(request.form["x"]), int(request.form["y"]))
        elif request.form["submit"] == "multiply":
            print("I'm multiplying")
            mul.delay(int(request.form["x"]), int(request.form["y"]))
    
    return render_template("run.html")

@bp.route("/<specimen_id>/<section_num>/<session_id>/convert_to_gif", methods=('GET', 'POST'))
def convert_to_gif(specimen_id, section_num, session_id):
    db = get_db()
    

@bp.route("/<specimen_id>/<section_num>/<session_id>/convert_to_n5", methods=('GET', 'POST'))
def convert_to_n5(specimen_id, section_num, session_id):
    pass

@bp.route("/<specimen_id>/<section_num>/<session_id>/convert_to_gif", methods=('GET', 'POST'))
def convert_to_bdv(specimen_id, section_num, session_id):
    pass