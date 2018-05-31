# coding=utf-8
import udatetime
from app import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.plugins.auth.models import Groups, Group
from app.plugins.tasks.routes import tasks_page
from app.plugins.Horatio.forms import CreateCase
from app.plugins.Horatio.globals import AVAILABLE_CHOICES
from app.plugins.Horatio.models import Cases, Detection
from app.plugins.analysis.routes import get_upload_file_hash
from app.plugins.analysis.file.upload import allowed_file
from werkzeug.utils import secure_filename

cases = Blueprint('cases', __name__, template_folder='templates')


@tasks_page.route('/cases', methods=['GET'])
@login_required
def cases_plugin_route():
    """the tasks function returns the plugin framework for the yara_plugin default task view"""
    # TODO show current cases in the database
    page = request.args.get('page', 1, type=int)
    case_list = Cases.query.all()
    return render_template('cases.html', title='Cases Plugin', page=page, case_list=case_list)


@tasks_page.route('/create', methods=['GET', 'POST'])
@login_required
def create_case_route():
    """Create case default view."""
    group_info = Groups.query.all()
    if request.method == 'POST':
        form = CreateCase(request.form)
        form.detection_method.choices = AVAILABLE_CHOICES
        if form.validate():
            try:
                file = request.files['file']
            except KeyError:
                file = None
            if file and allowed_file(file.filename):
                secure_filename(file.filename)
                get_upload_file_hash(file)
            detection_method_selection = None
            for items in AVAILABLE_CHOICES:
                if items[0] == form.detection_method.data[0]:
                    detection_method_selection = items
            new_case = Cases(case_name=form.name.data, description=form.description.data, subject=form.subject.data,
                             created_by=current_user.id, case_status="New Issue",
                             detection_method=detection_method_selection[1], group_access=form.group_access.data,
                             created_time_stamp=udatetime.utcnow(), modify_time_stamp=udatetime.utcnow())
            db.session.add(new_case)
            db.session.commit()
            flash("The case has been created.")
            return redirect(url_for('tasks.cases_plugin_route'))
    form = CreateCase(request.form)
    return render_template('create_case.html', title='Create Case', form=form, groups=group_info,
                           detection_method=AVAILABLE_CHOICES)

@tasks_page.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_case_route():
    """Edit case view."""
    group_info = Groups.query.all()
    case_id = request.args.get("case_id")
    user_id = Group.query.filter_by(username_id=current_user.id).all()
    allowed = False
    for user_group in user_id:
        if user_group.groups_id == case_id:
            allowed = True

    # group_info = Groups.query.filter_by(user_id=)
    if request.method == 'POST':
        if allowed:
            form = CreateCase(request.form)
        else:
            return
    if request.method == "GET":
        if allowed:
            form = CreateCase(request.form)
            return render_template('create_case.html', title='Edit Case', form=form, groups=group_info,
                                   detection_method=AVAILABLE_CHOICES)
        else:
            return cases_plugin_route()
        # for user in user_id:
        #     cases.append(Cases.query.filter_by(group_access=user.groups_id))


