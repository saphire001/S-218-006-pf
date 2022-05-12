import csv
import logging
import os

from flask import Blueprint, render_template, abort, url_for, current_app
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename, redirect

from app.db import db
from app.db.models import Transactions
from app.transactions.forms import csv_upload

transactions = Blueprint('transactions', __name__, template_folder='templates')


@transactions.route('/transactions', methods=['GET'], defaults={"page": 1})
@transactions.route('/transactions/<int:page>', methods=['GET'])
def transactions_browse(page):
    page = page
    per_page = 1000
    pagination = Transactions.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    try:
        return render_template('browse_transactions.html', data=data, pagination=pagination, balance=current_user.balance)
    except TemplateNotFound:
        abort(404)


@transactions.route('/transactions/upload', methods=['POST', 'GET'])
@login_required
def transactions_upload():
    form = csv_upload()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        form.file.data.save(filepath)

        list_of_transactions = []
        total_transactions = 0
        with open(filepath, encoding='utf-8-sig') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                current_transaction = Transactions(row['AMOUNT'], row['TYPE'])
                list_of_transactions.append(current_transaction)
                total_transactions = total_transactions + int(current_transaction.amount)

        current_user.transactions += list_of_transactions
        current_user.add_balance(total_transactions)

        db.session.commit()

        log = logging.getLogger("myApp")
        current_app.logger.info(f"\t-- {len(current_user.transactions)} Transaction(s) Uploaded by {current_user}. Check myApp.log --")
        current_user.set_balance(current_user.balance)
        db.session.commit()
        current_app.logger.info(f"current user bal: {current_user.balance}")
        log.info(f"\t-- {len(current_user.transactions)} Transaction(s) Uploaded by current user {current_user} w/ balance {current_user.balance} --")

        return redirect(url_for('transactions.transactions_browse'))

    try:
        return render_template('upload.html', form=form)
    except TemplateNotFound:
        abort(404)
