from flask_wtf import FlaskForm
from wtforms.fields import (
    DateField,
    EmailField,
    PasswordField,
)
from wtforms import validators, ValidationError


def password_validator(_, field):
    if not len(set(field.data)) > 5:
        raise ValidationError("Password must contain at least 5 unique character.")


class RegisterForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            validators.Email("Invalid email address."),
            validators.DataRequired("Please Enter your Email."),
        ],
        render_kw={
            "autocomplete": "email",
            "title": "Your email, e.g. example@gmail.com",
        },
        filters=[lambda s: s.strip().lower() if s else s],
    )
    birthdate = DateField(
        "Birthdate",
        validators=[validators.DataRequired("Please fill this field.")],
        render_kw={"autocomplete": "bday"},
    )
    password = PasswordField(
        "Password",
        validators=[
            password_validator,
            validators.Length(8, 64, "Password must be 8-64 characters."),
            validators.DataRequired("Please create a password."),
        ],
        render_kw={
            "autocomplete": "new-password",
            "title": "Your account password, make it strong!",
        },
    )
    confirm_password = PasswordField(
        "Confirm Your Password",
        validators=[
            validators.DataRequired("Please confirm your password."),
            validators.EqualTo("password", "Passwords don't match."),
        ],
        render_kw={
            "autocomplete": "new-password",
            "title": "Repeat your password again.",
        },
    )

    def is_required(self, field):
        return any(isinstance(v, validators.DataRequired) for v in field.validators)


class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            validators.DataRequired("Please Enter your email address."),
        ],
        render_kw={"autocomplete": "email"},
        filters=[lambda s: s.strip().lower() if s else s],
    )
    password = PasswordField(
        "Password",
        validators=[
            validators.DataRequired("Please enter your password"),
        ],
        render_kw={"autocomplete": "current-password"},
    )

    def is_required(self, field) -> bool:
        return any(isinstance(v, validators.DataRequired) for v in field.validators)
