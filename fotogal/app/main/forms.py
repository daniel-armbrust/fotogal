#
# fotogal/app/main/forms.py
#

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms import TextAreaField, BooleanField, validators, ValidationError


class RegistrationForm(FlaskForm):
    """Registration Form

    """
    email = StringField('Email', [
        validators.Email(message=(u'Endereço de e-mail está inválido.')),
        validators.DataRequired()
    ])

    full_name = StringField('Nome Completo', [
        validators.Length(min=10, max=500, message=u'Nome completo está inválido.'),
        validators.DataRequired()
    ])

    username = StringField('Username', [
        validators.Regexp('\w+$', message=u'Apenas letras, números ou sublinhado são permitidos.'),
        validators.Length(min=4, max=30, message=u'Nome de usuário inválido.'),
        validators.DataRequired()
    ])

    password = PasswordField('Senha', [
        validators.Length(min=10, max=50, message=u'A senha deve ter no mínimo 10 caracteres de comprimento.'),
        validators.DataRequired()
    ])

    submit = SubmitField(u'Cadastrar')

    def validate_email(self, field):
      pass

    def validate_username(self, field):
      pass


class ProfileForm(FlaskForm):
    """User Profile Form

    """
    full_name = StringField('Nome', [
        validators.Length(min=10, max=500),
        validators.DataRequired()
    ])

    username = StringField('Username', [
        validators.Length(min=4, max=30, message=u'Nome de usuário inválido!'),
        validators.DataRequired()
    ], render_kw={'readonly': 'readonly'})

    email = StringField('Email', [
        validators.Email(message=(u'Endereço de e-mail inválido!')),
        validators.DataRequired()
    ], render_kw={'readonly': 'readonly'})  

    gender = SelectField('Gênero', 
        choices=[('maculino', u'Masculino',), 
           ('feminino', u'Feminino',), ('prefiro_nao_dizer', u'Prefiro não dizer')]) 

    website = StringField('Site', [
        validators.Optional(),
        validators.Regexp(r'^(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.]))', message=u'Site inválido!')        
    ]) 

    bio = TextAreaField('Biografia', [
        validators.Length(min=0, max=3000),
    ])

    is_private = BooleanField('Conta privada')


class ProfilePasswdForm(FlaskForm):
    """User Profile Password Form

    """
    old_password = PasswordField('Senha antiga', [
        validators.Length(min=10, max=50, message=u'Senha inválida!'),
        validators.DataRequired()
    ])

    new_password = PasswordField('Nova senha', [
        validators.Length(min=10, max=50, message=u'Senha inválida!'),
        validators.DataRequired(),
        validators.EqualTo('confirm_new_password', message='As senhas devem ser iguais!')
    ])

    confirm_new_password = PasswordField('Confirmar nova senha')