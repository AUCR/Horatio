"""AUCR case plugin default page forms."""
# coding=utf-8
from flask import flash

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, DataRequired
from flask_babel import _, lazy_gettext as _l
from app.plugins.tasks.models import TaskCategory


class CreateCase(FlaskForm):
    """Crease Case Form."""
    subject = TextAreaField(_l('Subject'), validators=[Length(min=0, max=256)])
    description = TextAreaField(_l('Description'), validators=[Length(min=0, max=256)])
    category = TaskCategory()
    submit = SubmitField(_l('Create'))
