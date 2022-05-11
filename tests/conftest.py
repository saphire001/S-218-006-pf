import logging
import os
import pytest

from app import create_app, User
from app.db import db
from flask import current_app

@pytest.fixture()
def application():
    """This makes the app"""
    # os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_ENV'] = 'testing'

    application = create_app()

    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        # drops the database tables after the test runs
        db.drop_all()


@pytest.fixture()
def add_user(application):
    with application.app_context():
        # new record
        user = User('keith@webizly.com', 'testtest', True)
        db.session.add(user)
        db.session.commit()


@pytest.fixture()
def runner(application):
    """This makes the task runner"""
    return application.test_cli_runner()


@pytest.fixture()
def client(application):
    """This makes the http client"""
    return application.test_client()