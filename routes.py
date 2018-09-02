# coding=utf-8
import udatetime
from app import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.plugins.auth.models import Groups, Group, User
from app.plugins.Horatio.forms import CreateCase, EditCase, SaveCase
from app.plugins.Horatio.globals import AVAILABLE_CHOICES
from app.plugins.Horatio.models import Cases, Detection
from app.plugins.tasks.models import TaskStates
from app.plugins.analysis.routes import get_upload_file_hash
from app.plugins.analysis.file.upload import allowed_file
from werkzeug.utils import secure_filename
from sqlalchemy import or_

cases_page = Blueprint('cases', __name__, template_folder='templates')


@cases_page.route('/cases', methods=['GET'])
@login_required
def cases_plugin_route():
    """the tasks function returns the plugin framework for the yara_plugin default task view"""
    # TODO show current cases in the database
    page = request.args.get('page', 1, type=int)
    case_list = Cases.query.all()
    case_dict = {}

    # Current state choices
    count = 0
    state_choices = []
    for state in TaskStates.query.all():
        count += 1
        state_choices.append((int(count), state.task_state_name))
    # User choices
    user_choices = []
    for user in User.query.all():
        # Just keep admin out of the list
        if user.id == 1:
            continue
        else:
            user_choices.append((user.id, user.username))

    for item in case_list:
        # Get the actual value of the status
        case_status_value = item.case_status
        for items in state_choices:
            if items[0] == item.case_status:
                case_status_value = items[1]
        # Get the actual value of the detection
        detection_method_value = item.detection_method
        for items in AVAILABLE_CHOICES:
            if items[0] == item.detection_method:
                detection_method_value = items[1]
        # Get the actual value of the assigned user
        assigned_user_value = item.assigned_to
        for items in user_choices:
            if items[0] == item.assigned_to:
                assigned_user_value = items[1]
        group_access_value = Group.query.filter_by(username_id=current_user.id, groups_id=item.group_access).first()
        if group_access_value:
            item_dict = {"id": item.id, "status": case_status_value,
                         "subject": item.subject, "description": item.description,
                         "detection": detection_method_value, "last_modified": item.modify_time_stamp,
                         "assigned_to": assigned_user_value}

            case_dict[str(item.id)] = item_dict

    return render_template('cases.html', title='Cases Plugin', page=page, case_list=case_list, table_dict=case_dict)


@cases_page.route('/create', methods=['GET', 'POST'])
@login_required
def create_case_route():
    """Create case default view."""
    group_info = Groups.query.all()
    # User choices
    user_choices = []
    for user in User.query.all():
        # Just keep admin out of the list
        if user.id == 1:
            continue
        else:
            user_choices.append((user.id, user.username))

    if request.method == 'POST':
        form = CreateCase(request.form)
        form.detection_method.choices = AVAILABLE_CHOICES
        file_hash = None
        if form.validate():
            try:
                file = request.files['file']
            except KeyError:
                file = None
            if file and allowed_file(file.filename):
                secure_filename(file.filename)
                file_hash = get_upload_file_hash(file)
            detection_method_selection = None
            for items in AVAILABLE_CHOICES:
                if items[0] == form.detection_method.data[0]:
                    detection_method_selection = items
            new_case = Cases(description=form.description.data, subject=form.subject.data,
                             created_by=current_user.id, case_status=4,
                             detection_method=detection_method_selection[1], group_access=form.group_access.data[0],
                             created_time_stamp=udatetime.utcnow(), modify_time_stamp=udatetime.utcnow(),
                             attached_files=file_hash, assigned_to=form.assigned_to.data[0])
            db.session.add(new_case)
            db.session.commit()
            flash("The case has been created.")
            return redirect(url_for('cases.cases_plugin_route'))
    form = CreateCase(request.form)
    return render_template('create_case.html', title='Create Case', form=form, groups=group_info,
                           detection_method=AVAILABLE_CHOICES, assigned_to=user_choices)


@cases_page.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_case_route():
    """Edit case view."""
    # Group info
    group_info = Groups.query.all()
    submitted_case_id = request.args.get("id")
    group_ids = Group.query.filter_by(username_id=current_user.id).all()
    user_groups = []
    for user_group in group_ids:
        user_groups.append(user_group.groups_id)
    # Current state choices
    count = 0
    state_choices = []
    for state in TaskStates.query.all():
        count += 1
        state_choices.append((int(count), state.task_state_name))
    # User choices
    user_choices = []
    for user in User.query.all():
        # Just keep admin out of the list
        if user.id == 1:
            continue
        else:
            user_choices.append((user.id, user.username))

    case = Cases.query.filter_by(id=submitted_case_id)
    case = case.filter(or_(Cases.id == submitted_case_id, Cases.group_access.in_(user_groups))).first()
    if request.method == 'POST':
        if case:
            form = EditCase(request.form)
            if form.validate_on_submit():
                if case is not None:
                    case.subject = request.form["subject"]
                    case.description = request.form["description"]
                    case.case_notes = request.form["case_notes"]
                    case.case_rules = request.form["case_rules"]
                    case.detection_method = int(request.form["detection_method"])
                    case.case_status = int(request.form["case_status"])
                    case.assigned_to = int(request.form["assigned_to"])
                    case.group_access = int(request.form["group_access"])
                    db.session.commit()
            else:
                for error in form.errors:
                    flash(str(form.errors[error][0]), 'error')
                render_template('register.html', title=_('Register'), form=form)
        return cases_plugin_route()
    if request.method == "GET":
        if case:
            form = EditCase(case)
            # Get the actual value of the status
            case_status_value = case.case_status
            group_access_value = Group.query.filter_by(username_id=current_user.id, groups_id=case.group_access).first()
            if group_access_value:
                group_choices = []
                for group in Groups.query.all():
                    group_choices.append((int(group.id), group.name))
                for items in state_choices:
                    if items[0] == case.case_status:
                        case_status_value = items[1]
                # Get the actual value of the detection
                detection_method_value = case.detection_method
                for items in AVAILABLE_CHOICES:
                    if items[0] == case.detection_method:
                        detection_method_value = items[1]
                # Get the actual value of the assigned user
                assigned_user_value = case.assigned_to
                for items in user_choices:
                    if items[0] == case.assigned_to:
                        assigned_user_value = items[1]
                assigned_group_value = None
                for items in group_choices:
                    if items[0] == case.group_access:
                        assigned_group_value = items[1]
                table_dict = {"id": case.id, "subject": case.subject, "description": case.description,
                              "detection": detection_method_value, "status": case_status_value,
                              "case_notes": case.case_notes, "case_rules": case.case_rules,
                              "assigned_to": assigned_user_value, "group_access": assigned_group_value}
                return render_template('edit_case.html', title='Edit Case', form=form, groups=group_info,
                                       detection_method=AVAILABLE_CHOICES, case_status=state_choices,
                                       assigned_to=user_choices, table_dict=table_dict, groups_access=group_choices)
            return cases_plugin_route()
        else:
            return cases_plugin_route()
