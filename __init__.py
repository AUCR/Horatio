"""AUCR Horatio IR Case Management System plugin framework."""
# coding=utf-8
from app.plugins.Horatio.routes import cases


def load(app):
    """load overrides for Tasks plugin to work properly"""
    app.register_blueprint(cases, url_prefix='/cases')
