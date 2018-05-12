# coding=utf-8
from app import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.plugins.auth.models import Groups
from app.plugins.tasks.routes import tasks_page
from app.plugins.Horatio.forms import CreateCase
from app.plugins.Horatio.globals import AVAILABLE_CHOICES
from app.plugins.Horatio.models import Cases
from app.plugins.auth.utils import get_groups

cases = Blueprint('cases', __name__, template_folder='templates')


@tasks_page.route('/cases', methods=['GET'])
@login_required
def cases_plugin_route():
    """the tasks function returns the plugin framework for the yara_plugin default task view"""
    # TODO show current cases in the database
    current_user_groups = get_groups()
    page = request.args.get('page', 1, type=int)
    case_list = Cases.query.all()
    return render_template('cases.html', title='Cases Plugin',
                           page=page, render_current_user_groups=current_user_groups, case_list=case_list)


@tasks_page.route('/create', methods=['GET', 'POST'])
@login_required
def create_case_route():
    """Create case default view"""
    form = CreateCase(request.form)
    if request.method == 'POST':
        form.detection_method.choices = AVAILABLE_CHOICES
        if form.validate():
            detection_method_selection = None
            for items in AVAILABLE_CHOICES:
                if items[0] == form.detection_method.data[0]:
                    detection_method_selection = items
            new_case = Cases(description=form.description.data, subject=form.subject.data,
                             created_by=current_user.id, case_status="New Issue",
                             detection_method=detection_method_selection[1], group_access=form.group_access.data)
            db.session.add(new_case)
            db.session.commit()
            flash("The case has been created.")
            return redirect(url_for('tasks.cases_plugin_route'))
    group_info = Groups.query.all()
    current_user_groups = get_groups()
    return render_template('create_case.html', title='Create Case', form=form, groups=group_info,
                           render_current_user_groups=current_user_groups)

