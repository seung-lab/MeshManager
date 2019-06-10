from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, SelectField, RadioField, HiddenField
from wtforms.validators import DataRequired
from webservices.utils import get_datasets

class datasetForm(FlaskForm):
    dataset = SelectField('dataset', choices=[], validators=[DataRequired()])
    version = SelectField('version', choices=[], validators=[DataRequired()])
    somapt_x = DecimalField('somapt_x', validators=[DataRequired()])
    somapt_y = DecimalField('somapt_y', validators=[DataRequired()])
    somapt_z = DecimalField('somapt_z', validators=[DataRequired()])

class skeletonizeForm(FlaskForm):
    dataset = SelectField('dataset', choices=[], validators=[DataRequired()])
    version = SelectField('version', choices=[], validators=[DataRequired()])
    root_id = StringField('root_id', validators=[DataRequired()])
    want_soma_pt = RadioField('Input Soma Point', id="want_soma_pt", choices=[('1', 'Yes'), ('0', 'No')], default='0')
    somapt_x = DecimalField('somapt_x', default=-1)
    somapt_y = DecimalField('somapt_y', default=-1)
    somapt_z = DecimalField('somapt_z', default=-1)
    submit = SubmitField('Submit')

class skeletonViewerForm(FlaskForm):
    swc_input = HiddenField('swc_input')
    