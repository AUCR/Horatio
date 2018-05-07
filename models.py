"""db.py is the cases plugin database library for all task plugins to use"""
# coding=utf-8
import udatetime as datetime
from app import db
from yaml_info.yamlinfo import YamlInfo


class Cases(db.Model):
    """Case data default table for aucr."""

    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True)
    case_name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    detection_method = db.Column(db.String(32), index=True)
    # TODO make subject pull from task subject table
    subject = db.Column(db.String(256))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_access = db.Column(db.Integer, db.ForeignKey('groups.id'))
    case_status = db.Column(db.String(128))

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
    run = YamlInfo("app/plugins/Horatio/detection_methods.yml", "none", "none")
    detection_data = run.get()
    for items in detection_data:
        new_detection_table_row = Detection(detection_method=items)
        db.session.add(new_detection_table_row)
        db.session.commit()


db.event.listen(Detection.__table__, 'after_create', insert_initial_detection_values)
