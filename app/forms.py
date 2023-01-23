from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from wtforms.csrf.session import SessionCSRF


class UserCreationForm(FlaskForm):
    firstName = StringField("Username", validators = [DataRequired()])
    lastName = StringField("Username", validators = [DataRequired()])
    username = StringField("Username", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField()

class EditAccountForm(FlaskForm):
    firstName = StringField("First Name", validators=[DataRequired()])
    lastName = StringField("Last Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField()

class PokemonForm(FlaskForm):
    pokemon = StringField("Pokemon name or number", validators = [DataRequired()])
    submit = SubmitField()




