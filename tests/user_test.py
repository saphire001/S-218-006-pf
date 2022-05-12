#import logging

#from app import db
#from app.db.models import User, Transactions
from app.auth.forms import *

# def test_adding_user(application):
#     log = logging.getLogger("myApp")
#     with application.app_context():
#         assert db.session.query(User).count() == 0
#         assert db.session.query(Transactions).count() == 0
#
#         user = User('keith@webizly.com', 'testtest', True)
#         db.session.add(user)
#
#         user = User.query.filter_by(email='keith@webizly.com').first()
#         log.info(user)
#
#         assert user.email == 'keith@webizly.com'
#
#         user.transactions = [Transactions(12343, 'Credit'), Transactions(1243, 'Debit')]
#         db.session.commit()
#
#         assert db.session.query(Transactions).count() == 2
#
#         transaction1 = Transactions.query.filter_by(amount = '12343')
#         assert transaction1.amount == '12343'
#
#         transaction1.amount = '12543'
#         db.session.commit()
#
#         transaction2 = Transactions.query.filter_by(amount = '12543')
#         assert transaction2.amount == '12543'
#
#         db.session.delete(user)
#         assert db.session.query(User).count() == 0
#         assert db.session.query(Transactions).count() == 0
