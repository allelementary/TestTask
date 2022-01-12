from wtforms import Form, StringField, PasswordField, validators


class RegisterForm(Form):
    email = StringField('Email', [validators.Length(min=6, max=50)])
    first_name = StringField('First name', [validators.Length(min=1, max=50)])
    last_name = StringField('Last name', [validators.Length(min=1, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
