# coding=utf-8
from flask import Blueprint, render_template
from flask_login import login_required
from app.plugins.tasks.routes import tasks_page
from app.plugins.Horatio.forms import CreateCase

cases = Blueprint('cases', __name__, template_folder='templates')


@tasks_page.route('/cases', methods=['GET'])
@login_required
def cases_plugin_route():
    """the tasks function returns the plugin framework for the yara_plugin default task view"""
    return render_template('cases.html', title='Cases Plugin')


@tasks_page.route('/create', methods=['GET'])
@login_required
def create_case_route():
    """Create case default view"""
    form = CreateCase()
    return render_template('create_case.html', title='Create Case', form=form)
