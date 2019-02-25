"""db.py is the cases plugin database library for all task plugins to use"""
# coding=utf-8
import udatetime as datetime
from aucr_app import db
from yaml_info.yamlinfo import YamlInfo
from aucr_app.plugins.auth.models import SearchableMixin


class Cases(SearchableMixin, db.Model):
    """Case data default table for aucr."""

    __searchable__ = ['id', 'description', 'modify_time_stamp', 'detection_method', 'subject', 'case_notes',
                      'case_rules', 'created_by', 'assigned_to', 'group_access', 'attached_files',  'case_status']
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), index=True)
    created_time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modify_time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    detection_method = db.Column(db.String(32), index=True)
    subject = db.Column(db.String(256))
    case_notes = db.Column(db.String(3072))
    case_rules = db.Column(db.String(3072))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_access = db.Column(db.Integer, db.ForeignKey('groups.id'))
    md5_hash = db.Column(db.String(32), db.ForeignKey('uploaded_file_table.md5_hash'))
    case_status = db.Column(db.Integer, db.ForeignKey('task_states.id'))

    def __repr__(self):
        return '<Cases {}>'.format(self.id)

    def to_dict(self):
        """Return dictionary object type for API calls."""
        data = {
            'id': self.id,
            'description': self.description,
            'created_time_stamp': self.created_time_stamp.isoformat() + 'Z',
            'modify_time_stamp': self.modify_time_stamp.isoformat() + 'Z',
            'detection_method': self.detection_method,
            'subject': self.subject,
            'case_notes': self.case_notes,
            'case_rules': self.case_rules,
            'created_by': self.created_by,
            'assigned_to': self.assigned_to,
            'group_access': self.group_access,
            'md5_hash': self.md5_hash,
            'case_status': self.case_status
        }
        return data


class Detection(db.Model):
    """Detection method data default table for aucr."""

    __tablename__ = 'detection'
    id = db.Column(db.Integer, primary_key=True)
    detection_method = db.Column(db.String(32), index=True)
    description = db.Column(db.String(256), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Detection {}>'.format(self.detection_method)


def insert_initial_detection_values(*args, **kwargs):
    """Insert Task category default database values from a yaml template file."""
    detection_run = YamlInfo("aucr_app/plugins/Horatio/detection_methods.yml", "none", "none")
    detection_data = detection_run.get()
    for items in detection_data:
        new_detection_table_row = Detection(detection_method=items)
        db.session.add(new_detection_table_row)
        db.session.commit()


db.event.listen(Detection.__table__, 'after_create', insert_initial_detection_values)
