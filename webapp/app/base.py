from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for
)

bp = Blueprint('base', __name__)

@bp.route('/')
def base():
    return render_template("base.html")