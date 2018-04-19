"""AUCR case plugin default page forms."""
# coding=utf-8
from flask import flash

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, DataRequired
from flask_babel import _, lazy_gettext as _l
from app.plugins.Horatio.globals import AVAILABLE_CHOICES

# AVAILABLE_CHOICES = [('1', 'User Reported'), ('2', 'AV')]
DEFAULT_CHOICES = []


class CreateCase(FlaskForm):
    """Crease Case Form."""
    subject = TextAreaField(_l('Subject'), validators=[Length(min=0, max=256)])
    description = TextAreaField(_l('Description'), validators=[Length(min=0, max=256)])
    detection_method = SelectMultipleField('Detection Method', choices=AVAILABLE_CHOICES)
    submit = SubmitField(_l('Create'))
