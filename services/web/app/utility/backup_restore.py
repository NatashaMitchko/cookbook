import os, json

from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import BooleanField, SubmitField

from app.model.recipe import get_recipe_object


class RecipeBackupFileForm(FlaskForm):
    backup = FileField(validators=[FileRequired()])
    restore = BooleanField("Yes")
    submit = SubmitField("Save")


def restore_from_backup(filename) -> int:
    backup = os.path.join(current_app.config["BACKUP_FOLDER"], filename)
    failure_count = 0
    with open(backup) as b:
        while line := b.readline():
            try:
                data = json.loads(line.rstrip())
                r = get_recipe_object(data)
                r.save()
            except:
                failure_count += 1
    return failure_count
