from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def dashboard():

    account = current_user.account

    cash = account.cash_balance

    bank = account.bank_balance

    total = cash + bank

    return render_template(
        "dashboard.html",
        cash=cash,
        bank=bank,
        total=total
    )