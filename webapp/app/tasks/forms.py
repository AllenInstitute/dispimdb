from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, InputRequired

class GifGenerationForm(FlaskForm):
    pass

class TiffToN5Form(FlaskForm):
    pass

class N5ToTiffForm(FlaskForm):
    pass

class N5DownsampleForm(FlaskForm):
    pass

class N5ScalePyramidForm(FlaskForm):
    pass