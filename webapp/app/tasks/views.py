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
from app.tasks import celery
from . import bp

@bp.route("/<specimen_id>/<section_num>/<session_id>/overview_gif", methods=("GET", "POST"))
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
            celery.add.delay(int(request.form["x"]), int(request.form["y"]))
        elif request.form["submit"] == "multiply":
            print("I'm multiplying")
            celery.mul.delay(int(request.form["x"]), int(request.form["y"]))
    
    return render_template("run.html")
    # return redirect()

@bp.route("/<specimen_id>/<section_num>/<session_id>/convert_to_gif", methods=('GET', 'POST'))
def convert_to_gif(specimen_id, section_num, session_id):
    pass

@bp.route("/generate_gifs_ijm", methods=('GET', 'POST'))
def generate_gifs_ijm():
    db = get_db()
    sections = db.sections
    sessions = db.sessions

    '''
    section_dict = sections.find_one({
        "section_num": section_num,
        "specimen_id": specimen_id
    })

    session_dict = sessions.find_one({
        "session_id": session_id
    })

    print(section_dict['tiff_path'])
    print(section_dict['gif_path'])
    '''

    ijm_input = {
        'macro_path': '/home/samk/acworkflow/app/tasks/ijm_macros',
        'macro': 'test_batch.ijm',
        'args': {
            'tiff_path': '/mnt/c/Users/samrk/work_files/cortex_strip_1_ds',
            'gif_path': '/mnt/c/Users/samrk/work_files/cortex_strip_1_gifs'
        }
    }

    celery.generate_gifs_ijm.delay(ijm_input)

    return ""

@bp.route("/<specimen_id>/<section_num>/<session_id>/convert_to_gif", methods=('GET', 'POST'))
def generate_n5(specimen_id, section_num, session_id):
    pass

@bp.route("/<specimen_id>/<section_num>/<session_id>/convert_to_gif", methods=('GET', 'POST'))
def generate_bdv(specimen_id, section_num, session_id):
    pass