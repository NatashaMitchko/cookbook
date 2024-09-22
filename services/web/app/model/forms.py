from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    StringField,
    FieldList,
    RadioField,
    PasswordField,
    SubmitField,
)
from wtforms.validators import DataRequired, Optional, ValidationError
from flask_wtf.file import FileField, FileRequired

from app.model.recipe import is_valid_slug


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Register")


def ValidateSlug(form, field):
    if not is_valid_slug(field.data):
        raise ValidationError("Slug must not have spaces (e.g. this-is-a-slug)")


class RecipeForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired(), ValidateSlug])
    description = StringField("Description", validators=[Optional()])
    ingredients = FieldList(StringField("Ingredients"), min_entries=1)
    add_ingredient = SubmitField("Add Ingredient")
    steps = FieldList(StringField("Steps"), min_entries=1)
    add_step = SubmitField("Add Step")
    tags = FieldList(StringField("Tags"), min_entries=1)
    add_tag = SubmitField("Add Tag")
    status = RadioField("Status", choices=["Pending", "Published"])
    submit = SubmitField("Save")


class RecipeBackupFileForm(FlaskForm):
    backup = FileField(validators=[FileRequired()])
    restore = BooleanField("Yes")
    submit = SubmitField("Save")
