# coding=utf-8
from flask import Blueprint, render_template, request
from flask_login import login_required
from app.plugins.tasks.routes import tasks_page
from app.plugins.Horatio.forms import CreateCase
from app.plugins.tasks.models import TaskCategory

cases = Blueprint('cases', __name__, template_folder='templates')
test_list = [('1', 'Malware'), ('2', 'Spam'), ('3', 'Scam')]


@tasks_page.route('/cases', methods=['GET'])
@login_required
def cases_plugin_route():
    """the tasks function returns the plugin framework for the yara_plugin default task view"""
    return render_template('cases.html', title='Cases Plugin')


@tasks_page.route('/create', methods=['GET', 'POST'])
@login_required
def create_case_route():
    """Create case default view"""
    form = CreateCase(request.form)
    if request.method == 'POST':
        form.detection_method.choices = test_list

        if form.validate():
            return render_template("cases.html")
    return render_template('create_case.html', title='Create Case', form=form)
