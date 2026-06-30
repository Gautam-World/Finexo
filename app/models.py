from datetime import datetime

from flask_login import UserMixin

from app.extensions import db, bcrypt


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    account = db.relationship(
        "Account",
        backref="user",
        uselist=False,
        cascade="all, delete"
    )

    categories = db.relationship(
        "Category",
        backref="user",
        cascade="all, delete"
    )

    transactions = db.relationship(
        "Transaction",
        backref="user",
        cascade="all, delete"
    )

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(
            self.password_hash,
            password
        )


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    cash_balance = db.Column(
        db.Float,
        default=0
    )

    bank_balance = db.Column(
        db.Float,
        default=0
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(50),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    transactions = db.relationship(
        "Transaction",
        backref="category"
    )


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text)

    amount = db.Column(db.Float, nullable=False)

    date = db.Column(db.Date, nullable=False)

    transaction_type = db.Column(
        db.String(20),
        nullable=False
    )
    # Income | Expense | Transfer

    payment_method = db.Column(
        db.String(20),
        nullable=False
    )
    # Cash | Bank

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Transaction {self.title}>"