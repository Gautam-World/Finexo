from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    DecimalField,
    DateField,
    SelectField,
    SubmitField
)
from wtforms.validators import DataRequired


class TransactionForm(FlaskForm):

    date = DateField(
        "Date",
        validators=[DataRequired()]
    )

    transaction_type = SelectField(
        "Transaction Type",
        choices=[
            ("Income", "Income"),
            ("Expense", "Expense")
        ]
    )

    payment_method = SelectField(
        "Payment Method",
        choices=[
            ("Cash", "Cash"),
            ("Bank", "Bank")
        ]
    )

    category = SelectField(
        "Category",
        coerce=int
    )

    title = StringField(
        "Title",
        validators=[DataRequired()]
    )

    description = TextAreaField(
        "Description"
    )

    amount = DecimalField(
        "Amount",
        validators=[DataRequired()]
    )

    submit = SubmitField("Save Transaction")