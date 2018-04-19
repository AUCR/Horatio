# coding=utf-8
from app import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.plugins.tasks.routes import tasks_page
from app.plugins.Horatio.forms import CreateCase
from app.plugins.Horatio.globals import AVAILABLE_CHOICES
from app.plugins.Horatio.models import Cases


cases = Blueprint('cases', __name__, template_folder='templates')


@tasks_page.route('/cases', methods=['GET'])
@login_required
def cases_plugin_route():
    """the tasks function returns the plugin framework for the yara_plugin default task view"""
    # TODO show current cases in the database
    return render_template('cases.html', title='Cases Plugin')


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
                             detection_method=detection_method_selection[1])
            db.session.add(new_case)
            db.session.commit()
            flash("The case has been created.")
            return redirect(url_for('tasks.cases_plugin_route'))
    return render_template('create_case.html', title='Create Case', form=form)
