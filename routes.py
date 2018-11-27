# coding=utf-8
import udatetime
import logging
from aucr_app import db
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, g
from flask_login import login_required, current_user
from aucr_app.plugins.auth.models import Groups, Group, User
from aucr_app.plugins.Horatio.forms import CreateCase, EditCase, Horatio
from aucr_app.plugins.Horatio.globals import AVAILABLE_CHOICES
from aucr_app.plugins.Horatio.models import Cases
from aucr_app.plugins.tasks.models import TaskStates
from aucr_app.plugins.analysis.routes import get_upload_file_hash
from aucr_app.plugins.analysis.file.upload import allowed_file
from werkzeug.utils import secure_filename
from multiprocessing import Process
from sqlalchemy import or_
from aucr_app.plugins.tasks.mq import index_mq_aucr_task, get_mq_yaml_configs, index_mq_aucr_report

cases_page = Blueprint('cases', __name__, template_folder='templates')


def process_case(case_id):
    """MQ Process file."""
    index_mq_aucr_task(rabbit_mq_server=current_app.config['RABBITMQ_SERVER'], task_name=case_id, routing_key="cases")


@cases_page.route('/search')
@login_required
def search():
    """AUCR search plugin flask blueprint."""
    if not g.search_form.validate():
        return redirect(url_for('cases.cases'))
    page = request.args.get('page', 1, type=int)
    posts, total = Cases.search(g.search_form.q.data, page, int(current_app.config['POSTS_PER_PAGE']))
    cases, total = Cases.search(g.search_form.q.data, page, int(current_app.config['POSTS_PER_PAGE']))
    next_url = url_for('search', q=g.search_form.q.data, page=page + 1) \
        if total > page * int(current_app.config['POSTS_PER_PAGE']) else None
    prev_url = url_for('search', q=g.search_form.q.data, page=page - 1) if page > 1 else None
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
    for posts in cases:
        print(posts)
    for item in cases:
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
    return render_template('cases.html', title='Case Search', page=page,
                           table_dict=case_dict, search_url='cases.search')


@cases_page.route('/cases', methods=['GET', 'POST'])
@login_required
def cases_plugin_route():
    """the tasks function returns the plugin framework for the yara_plugin default task view"""
    # TODO show current cases in the database
    if request.method == 'POST':
        return redirect("cases/create")
    case_dict = {}
    form = Horatio(request.form)
    page = request.args.get('page', 1, type=int)
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
    count = page * 10
    total = 0
    while total < 10:
        total += 1
        id_item = count - 10 + total
        item = Cases.query.filter_by(id=id_item).first()
        if item:
            group_ids = Group.query.filter_by(username_id=current_user.id).all()
            for group_items in group_ids:
                if item.group_access == group_items.groups_id:
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
                    item_dict = {"id": item.id, "status": case_status_value,
                                 "subject": item.subject, "description": item.description,
                                 "detection": detection_method_value, "last_modified": item.modify_time_stamp,
                                 "assigned_to": assigned_user_value}
                    case_dict[str(item.id)] = item_dict
    prev_url = '?page=' + str(page - 1)
    next_url = '?page=' + str(page + 1)
    return render_template('cases.html', title='Cases Plugin', page=page, case_list=case_dict, table_dict=case_dict,
                           search_url='cases.search', next_url=next_url, prev_url=prev_url , form=form)


@cases_page.route('/create', methods=['GET', 'POST'])
@login_required
def create_case_route():
    """Create case default view."""
    group_info = Groups.query.all()
    # User choices
    user_choices = []
    page = request.args.get('page', 1, type=int)
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
            return redirect(url_for('cases.cases_plugin_route', page=page))
    form = CreateCase(request.form)
    return render_template('create_case.html', title='Create Case', form=form, groups=group_info,
                           detection_method=AVAILABLE_CHOICES, assigned_to=user_choices,  search_url='cases.search')


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
                    rabbit_mq_server_ip = current_app.config['RABBITMQ_SERVER']
                    mq_config_dict = get_mq_yaml_configs()
                    files_config_dict = mq_config_dict["reports"]
                    for item in files_config_dict:
                        if "cases" in item:
                            logging.info("Adding a new case to the cases MQ" + " " + str(item["cases"][0]) + " to MQ")
                            index_mq_aucr_report(str(case.id), str(rabbit_mq_server_ip), item["cases"][0])
                    case_data = str(case.id)
                    p = Process(target=process_case, args=(case_data,))
                    p.start()
                    case.subject = request.form["subject"]
                    case.description = request.form["description"]
                    case.case_notes = request.form["case_notes"]
                    case.case_rules = request.form["case_rules"]
                    case.detection_method = int(request.form["detection_method"])
                    case.case_status = int(request.form["case_status"])
                    case.assigned_to = int(request.form["assigned_to"])
                    case.group_access = int(request.form["groups_access"])
                    db.session.commit()
            else:
                for error in form.errors:
                    flash(str(form.errors[error][0]), 'error')
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
                assigned_group_value = case.group_access
                for items in group_choices:
                    if items[0] == case.group_access:
                        assigned_group_value = items[1]
                table_dict = {"id": case.id, "subject": case.subject, "description": case.description,
                              "detection": detection_method_value, "status": case_status_value,
                              "case_notes": case.case_notes, "case_rules": case.case_rules,
                              "assigned_to": assigned_user_value, "group_access": assigned_group_value}
                return render_template('edit_case.html', title='Edit Case', form=form, groups=group_info,
                                       detection_method=AVAILABLE_CHOICES, case_status=state_choices,
                                       assigned_to=user_choices, table_dict=table_dict, groups_access=group_choices,
                                       search_url='cases.search')
            return cases_plugin_route()
        else:
            return cases_plugin_route()
