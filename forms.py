"""AUCR case plugin default page forms."""
# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectMultipleField, IntegerField
from wtforms.validators import Length
from flask_babel import lazy_gettext as _l
from app.plugins.Horatio.globals import AVAILABLE_CHOICES


class CreateCase(FlaskForm):
    """Crease Case Form."""
    subject = TextAreaField(_l('Subject'), validators=[Length(min=0, max=256)])
    description = TextAreaField(_l('Description'), validators=[Length(min=0, max=256)])
    detection_method = SelectMultipleField('Detection Method', choices=AVAILABLE_CHOICES)
    group_access = IntegerField(_l('Group Access'))
    submit = SubmitField(_l('Create'))
