"""db.py is the cases plugin database library for all task plugins to use"""
# coding=utf-8
import udatetime as datetime
from app import db
from yaml_info.yamlinfo import YamlInfo


class Cases(db.Model):
    """Case data default table for aucr."""

    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), index=True)
    created_time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modify_time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    detection_method = db.Column(db.String(32), index=True)
    subject = db.Column(db.String(256))
    case_notes = db.Column(db.String(4912))
    case_rules = db.Column(db.String(4912))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_access = db.Column(db.Integer, db.ForeignKey('groups.id'))
    attached_files = db.Column(db.String(128), db.ForeignKey('uploaded_file_table.file_hash'))
    case_status = db.Column(db.String(128), db.ForeignKey('task_states.task_state_name'))

    def __repr__(self):
        return '<Cases {}>'.format(self.case_name)

class Indicator(db.Model):
    __tablename__ = 'indicators'
    indicator_id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, index=True)
    point_value = db.Column(db.Integer)
    value = db.Column(db.String(256))
    type_id = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Indicator {}>'.format(self.point_value)

class Indicator_Type(db.Model):
    __tablename__ = 'indicator_types'
    indicator_type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))

    def __repr__(self):
        return '<Indicator_Type {}>'.format(self.name)

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
    detection_run = YamlInfo("app/plugins/Horatio/detection_methods.yml", "none", "none")
    indicator_run = YamlInfo("app/plugins/Horatio/indicator_types.yml", "none", "none")
    detection_data = detection_run.get()
    indicator_data= indicator_run.get()
    for items in detection_data:
        new_detection_table_row = Detection(detection_method=items)
        db.session.add(new_detection_table_row)
        db.session.commit()
    for items in indicator_data:
        new_indicator_table_row = Indicator_Type(name=items)
        db.session.add(new_indicator_table_row)
        db.session.commit()


db.event.listen(Detection.__table__, 'after_create', insert_initial_detection_values)
