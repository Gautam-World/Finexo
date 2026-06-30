from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models import Category

category_bp = Blueprint(
    "categories",
    __name__,
    url_prefix="/categories"
)


@category_bp.route("/")
@login_required
def categories():

    categories = Category.query.filter_by(
        user_id=current_user.id
    ).order_by(Category.name).all()

    return render_template(
        "categories.html",
        categories=categories
    )


@category_bp.route("/add", methods=["POST"])
@login_required
def add_category():

    name = request.form.get("name")

    if not name:
        flash("Category name is required.", "danger")
        return redirect(url_for("categories.categories"))

    existing = Category.query.filter_by(
        user_id=current_user.id,
        name=name
    ).first()

    if existing:
        flash("Category already exists.", "warning")
        return redirect(url_for("categories.categories"))

    category = Category(
        name=name,
        user_id=current_user.id
    )

    db.session.add(category)
    db.session.commit()

    flash("Category added successfully.", "success")

    return redirect(url_for("categories.categories"))


@category_bp.route("/delete/<int:id>")
@login_required
def delete_category(id):

    category = Category.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(category)
    db.session.commit()

    flash("Category deleted.", "info")

    return redirect(url_for("categories.categories"))