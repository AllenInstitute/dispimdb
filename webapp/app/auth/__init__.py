import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db
from app.forms import RegisterForm, LoginForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    db = get_db()
    users = db.users

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = ''

        if not username:
            error = error + 'Username is required. \n'
        if not password:
            error = error + 'Password is required. \n'
        
        if users.find({'username': username}).count() > 0:
            error = 'User {} is already registered'.format(username)
        
        if len(error) == 0:
            result = users.insert_one({
                'username': username,
                'password': generate_password_hash(password)
            })
            print(result)
            return redirect(url_for('auth.login'))
        
        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    db = get_db()
    users = db.users
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        error = None

        user = users.find_one({'username': username})
        print(user)

        if user is None or not check_password_hash(user['password'], password):
            error = 'Incorrect username or password.'
        
        if error is None:
            session.clear()
            session['user.username'] = user['username']
            return redirect(url_for('tracker.specimen_overview'))
        
        flash(error)

    return render_template('auth/login.html',
        form=form)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('tracker.specimen_overview'))

@bp.before_app_request
def load_logged_in_user():
    username = session.get('user.username')

    if username is None:
        g.user = None
    else:
        g.user = username

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)

    return wrapped_view