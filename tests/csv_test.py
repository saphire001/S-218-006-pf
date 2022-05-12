from app import db
from app.db.models import User, Transactions

def test_csv_upload(application):
    with application.app_context():
        db.session.query(User).count() == 0
        db.session.query(Transactions).count() == 0

        user = User('keith@webizly.com', 'testtest', True)
        db.session.add(user)

        user.transactions = [Transactions(12343,'Credit'), Transactions(1243, 'Debit')]
        db.session.commit()
        assert db.session.query(Transactions).count() == 2

        db.session.delete(user)
        assert db.session.query(User).count() == 0
        assert db.session.query(Transactions).count() == 0
