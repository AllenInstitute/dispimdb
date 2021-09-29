from flask import Blueprint, url_for

bp = Blueprint('tracker', __name__,
    url_prefix='/tracker',
    template_folder='templates')

from . import home, project, section, session, specimen, views