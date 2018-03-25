"""db.py is the cases plugin database library for all task plugins to use"""
# coding=utf-8
from datetime import datetime
from app import db
from yaml_info.yamlinfo import YamlInfo


class Cases(db.Model):
    """Case data default table for aucr."""

    # TODO add all the possible fields we should be using
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True)
    case_name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    subject = db.Column(db.String(256), db.ForeignKey('task_table.task_subject'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    case_status = db.Column(db.String(128), db.ForeignKey('task_states.task_state_name'))

    def __repr__(self):
        return '<Cases {}>'.format(self.case_name)


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
    run = YamlInfo("app/plugins/tasks/category.yaml", "none", "none")
    detection_data = run.get()
    for items in detection_data:
        new_detection_table_row = Detection(detection_method=items)
        db.session.add(new_detection_table_row)
        db.session.commit()


db.event.listen(Detection.__table__, 'after_create', insert_initial_detection_values)
