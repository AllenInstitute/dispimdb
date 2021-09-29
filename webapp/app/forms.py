from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, InputRequired

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    full_name = StringField('Full Name')
    position = StringField('Position')
    register = SubmitField('Register')
    cancel = SubmitField('Cancel')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class QueryForm(FlaskForm):
    project_id = StringField('Project ID')
    specimen_id = StringField('Specimen ID')

class DispimDbForm(FlaskForm):
    date_added = DateTimeField('Date Added')
    added_by = StringField('Added By')
    date_last_modified = DateTimeField('Last Modified')
    last_modified_by = StringField('Last Modified By')
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

class ProjectForm(DispimDbForm):
    project_id = StringField('Project ID', validators=[InputRequired()])
    lab_lead = StringField('Lab Lead', validators=[InputRequired()])
    description = StringField('Description')
    notes = StringField('Notes')

class SpecimenForm(FlaskForm):
    pass

class SectionForm(FlaskForm):
    pass

class ImagingSessionForm(FlaskForm):
    pass