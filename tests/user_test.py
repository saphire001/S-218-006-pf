
from app import db
from app.db.models import User
from app.auth.forms import *


def test_login(client):
    with client:
        user = User('keith@webizly.com', 'testtest', True)
        db.session.add(user)
        db.session.commit()

        response = client.get("/login")
        assert response.status_code == 200


def test_register(application, client):
    form = register_form()
    form.email.data = "keith@webizly.com"
    form.password.data = "testtest"
    form.confirm.data = "testtest"
    assert form.validate()


def test_login_dashboard(client):
    with client:
        response = client.get("/dashboard")
        assert response.status_code == 302


def test_logout_dashboard(client):
    db.session.query(User).count() == 0
    with client:
        response = client.get("/dashboard")
        assert b"<h1>Redirecting...</h1>" in response.data