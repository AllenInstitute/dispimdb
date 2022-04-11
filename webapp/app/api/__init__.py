from flask import Blueprint, url_for

bp = Blueprint('api', __name__,
    url_prefix='/api')

from . import routes