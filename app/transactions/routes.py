from datetime import date

from flask import Blueprint, render_template, redirect, url_for, flash

from flask_login import login_required, current_user

from app.extensions import db
from app.models import Transaction, Category
from app.transactions.forms import TransactionForm

transaction_bp = Blueprint(
    "transactions",
    __name__,
    url_prefix="/transactions"
)


@transaction_bp.route("/")
@login_required
def transactions():

    transactions = Transaction.query.filter_by(
        user_id=current_user.id
    ).order_by(Transaction.date.desc()).all()

    return render_template(
        "transactions.html",
        transactions=transactions
    )


@transaction_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_transaction():

    form = TransactionForm()

    categories = Category.query.filter_by(
        user_id=current_user.id
    ).order_by(Category.name).all()

    form.category.choices = [
        (c.id, c.name)
        for c in categories
    ]

    if form.date.data is None:
        form.date.data = date.today()

    if form.validate_on_submit():

        transaction = Transaction(
            title=form.title.data,
            description=form.description.data,
            amount=float(form.amount.data),
            date=form.date.data,
            transaction_type=form.transaction_type.data,
            payment_method=form.payment_method.data,
            user_id=current_user.id,
            category_id=form.category.data
        )

        db.session.add(transaction)

        account = current_user.account

        if transaction.transaction_type == "Income":

            if transaction.payment_method == "Cash":
                account.cash_balance += transaction.amount
            else:
                account.bank_balance += transaction.amount

        else:

            if transaction.payment_method == "Cash":
                account.cash_balance -= transaction.amount
            else:
                account.bank_balance -= transaction.amount

        db.session.commit()

        flash(
            "Transaction added successfully.",
            "success"
        )

        return redirect(
            url_for("transactions.transactions")
        )

    return render_template(
        "add_transaction.html",
        form=form
    )