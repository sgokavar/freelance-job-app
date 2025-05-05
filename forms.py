from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

class FreelancerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    skills = StringField('Skills', validators=[DataRequired()])
    availability = StringField('Availability', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ClientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')

class JobForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    pay_rate = StringField('Pay Rate', validators=[DataRequired()])
    client_id = SelectField('Client', coerce=int) 
    submit = SubmitField('Submit')
