"""AUCR case plugin default page forms."""
# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectMultipleField, IntegerField, StringField
from wtforms.validators import Length
from flask_babel import lazy_gettext as _l
from app.plugins.Horatio.globals import AVAILABLE_CHOICES


class CreateCase(FlaskForm):
    """Crease Case Form."""

    subject = TextAreaField(_l('Subject'), validators=[Length(min=0, max=256)])
    description = TextAreaField(_l('Description'), validators=[Length(min=0, max=256)])
    case_notes = TextAreaField(_l('Case Notes'), validators=[Length(min=0, max=4912)])
    current_state = SelectMultipleField('Status', choices=AVAILABLE_CHOICES)
    detection_method = SelectMultipleField('Detection Method', choices=AVAILABLE_CHOICES)
    group_access = SelectMultipleField(_l('Group Access'), choices=AVAILABLE_CHOICES)
    malicious_ips = TextAreaField(_l('Malicious Ips'), validators=[Length(min=0, max=256)])
    malicious_domains = TextAreaField(_l('Malicious Domains'), validators=[Length(min=0, max=256)])
    malicious_md5s = TextAreaField(_l('Malicious MD5s'), validators=[Length(min=0, max=256)])


    submit = SubmitField(_l('Create'))


class EditCase(FlaskForm):
    """Edit user profile settings."""

    case_id = IntegerField(_l('Case ID'), validators=[Length(min=0, max=12)])
    subject = TextAreaField(_l('Subject'), validators=[Length(min=0, max=256)])
    description = TextAreaField(_l('Description'), validators=[Length(min=0, max=256)])
    case_notes = TextAreaField(_l('Case Notes'), validators=[Length(min=0, max=4912)])
    case_rules = TextAreaField(_l('Case Rules'), validators=[Length(min=0, max=4912)])
    current_state = SelectMultipleField('Status', choices=AVAILABLE_CHOICES)
    detection_method = SelectMultipleField('Detection Method', choices=AVAILABLE_CHOICES)
    group_access = SelectMultipleField(_l('Group Access'), choices=AVAILABLE_CHOICES)
    submit = SubmitField(_l('Save'))
    malicious_ips = TextAreaField(_l('Malicious Ips'), validators=[Length(min=0, max=256)])
    malicious_domains = TextAreaField(_l('Malicious Domains'), validators=[Length(min=0, max=256)])
    malicious_md5s = TextAreaField(_l('Malicious MD5s'), validators=[Length(min=0, max=256)])

    def __init__(self, case, *args, **kwargs):
        """Edit user profile init self and return username."""
        super(EditCase, self).__init__(*args, **kwargs)
        try:
            self.case_id = case.id
            self.subject = case.subject
            self.description = case.description
            self.case_notes = case.case_notes
            self.case_rules = case.case_rules
            self.detection_method = case.detection_method
            self.group_access = case.group_access
        except:
            self.subject = case["subject"]
            self.description = case["description"]
            self.case_notes = case["case_notes"]
            self.case_rules = case["case_rules"]


class SaveCase(FlaskForm):
    """Edit user profile settings."""

    subject = TextAreaField(_l('Subject'), validators=[Length(min=0, max=256)])
    description = TextAreaField(_l('Description'), validators=[Length(min=0, max=256)])
    submit = SubmitField(_l('Save'))

    def __init__(self, case, *args, **kwargs):
        """Edit user profile init self and return username."""
        super(SaveCase, self).__init__(*args, **kwargs)
        self.subject = case.subject
        self.description = case.description
