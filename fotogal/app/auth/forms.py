#
# fotogal/app/auth/forms.py
#

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators


class LoginForm(FlaskForm):
    """Login Form

    """
    email = StringField('Email', [
        validators.Email(message=(u'Endereço de e-mail inválido!')),
        validators.DataRequired()
    ])

    password = PasswordField('Senha', [
        validators.Length(min=10, max=50, message=u'Senha inválida!'),
        validators.DataRequired()
    ])

    submit = SubmitField(u'Log In')