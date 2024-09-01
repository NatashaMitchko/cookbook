from enum import Enum
from typing import List
import json

from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, RadioField, SubmitField
from wtforms.validators import DataRequired, Optional

from app import redis_client


class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    description = StringField('Description', validators=[Optional()])
    ingredients = FieldList(StringField("Ingredients"), min_entries=1)
    add_ingredient = SubmitField("Add Ingredient")
    steps = FieldList(StringField("Steps"), min_entries=1)
    add_step = SubmitField("Add Step")
    tags = FieldList(StringField("Tags"), min_entries=1)
    add_tag = SubmitField("Add Tag")
    status = RadioField("Status", choices=["Pending", "Published"])
    submit = SubmitField("Save")

class PublishStatus(Enum):
    PENDING = 1
    PUBLISHED = 2


class Recipe:
    def __init__(
        self,
        title: str,
        slug: str,
        description: str,
        ingredients: List[str],
        steps: List[str],
        tags: List[str],
        status: PublishStatus,
    ) -> None:
        self.title = title
        self.slug = slug
        self.description = description
        self.ingredients = ingredients
        self.steps = steps
        self.tags = set(tags)
        self.status = status

    def save(self):
        recipe = {
            "title": self.title,
            "slug": self.slug,
            "description": self.description,
            "ingredients": self.ingredients,
            "steps": self.steps,
            "tags": list(self.tags),
            "status": self.status.name,
        }
        redis_client.set(self.slug, json.dumps(recipe))
