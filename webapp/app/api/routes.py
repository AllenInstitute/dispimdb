import logging

from flask import (
    jsonify
)

from app.db import get_db

from . import bp

@bp.route('/projects', methods=['GET'])
def get_projects():
    db = get_db()
    projects = db.projects

    project_cursor = projects.find({})
    project_list = []

    for project in project_cursor:
        project.pop('_id')
        project_list.append(project)
    
    return jsonify({'projects': project_list})

@bp.route('/project/<project_id>', methods=['GET'])
def get_project(project_id):
    db = get_db()
    projects = db.projects

    project = projects.find_one({'project_id': project_id})
    if project:
        project.pop('_id')
        return jsonify({'project': project})
    else:
        return jsonify({'error': 404}), 404

@bp.route('/specimens', methods=['GET'])
def get_specimens():
    db = get_db()
    specimens = db.specimens

    specimen_cursor = specimens.find({})
    specimen_list = []

    for specimen in specimen_cursor:
        specimen.pop('_id')
        specimen_list.append(specimen)
    
    return jsonify({'specimens': specimen_list})

@bp.route('/specimens/<specimen_id>', methods=['GET'])
def get_specimen(specimen_id):
    db = get_db()
    specimens = db.specimens

    specimen = specimens.find_one({'specimens': specimen_id})

    if specimen:
        specimen.pop('_id')
        return jsonify({'specimen': specimen})
    else:
        return jsonify({'error': 404}), 404

@bp.route('/specimens/<specimen_id>/sections', methods=['GET'])
def get_sections(specimen_id):
    db = get_db()
    sections = db.sections

    section_cursor = sections.find({'specimen_id': specimen_id})
    section_list = []

    for section in section_cursor:
        section.pop('_id')
        section_list.append(section)
    
    return jsonify({'sections': section_list})

@bp.route('/specimens/<specimen_id>/<section_num>', methods=['GET'])
def get_section(specimen_id, section_num):
    db = get_db()
    sections = db.sections

    section = sections.find_one({
        'specimen_id': specimen_id,
        'section_num': section_num
    })
    section.pop('_id')

    return jsonify({'section': section})