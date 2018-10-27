"""AUCR Horatio IR Case Management System plugin framework."""
# coding=utf-8
from aucr_app.plugins.Horatio.routes import cases_page
from aucr_app.plugins.Horatio.api.case import api_page as cases_api


def load(app):
    """load overrides for Tasks plugin to work properly"""
    app.register_blueprint(cases_page, url_prefix='/cases')
    app.register_blueprint(cases_api, url_prefix='/cases')
