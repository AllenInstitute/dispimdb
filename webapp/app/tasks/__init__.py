from flask import Blueprint, url_for

bp = Blueprint('tasks', __name__,
    url_prefix='/tasks',
    template_folder='templates')

from . import jobs, views