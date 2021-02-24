from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from webapp.models import User


class RegisterForm(FlaskForm):
    username = StringField('Gebruikersnaam',
                           validators=[DataRequired(message="Vul een naam in"),
                                       Length(min=2, max=20, message='')],
                           render_kw={'placeholder': 'Gebruikersnaam'})
    submit = SubmitField('Vul je voorspelling in')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Deze naam is al in gebruik')
        if len(username.data) < 2:
            raise ValidationError('Kies een langere naam')
        if len(username.data) > 20:
            raise ValidationError('Kies een kortere naam')


class LoginForm(FlaskForm):
    username = StringField('Gebruikersnaam',
                           validators=[DataRequired()],
                           render_kw={'placeholder': 'Gebruikersnaam'})
    pin = StringField('PIN',
                      validators=[DataRequired()],
                      render_kw={'placeholder': 'PIN'})
    submit = SubmitField('Log in')
