from enum import Enum
from typing import List
import json

from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, RadioField, SubmitField
from wtforms.validators import DataRequired, Optional

from app import redis_client

class PublishStatus(Enum):
    PENDING = 1
    PUBLISHED = 2


class RecipeForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    description = StringField("Description", validators=[Optional()])
    ingredients = FieldList(StringField("Ingredients"), min_entries=1)
    add_ingredient = SubmitField("Add Ingredient")
    steps = FieldList(StringField("Steps"), min_entries=1)
    add_step = SubmitField("Add Step")
    tags = FieldList(StringField("Tags"), min_entries=1)
    add_tag = SubmitField("Add Tag")
    status = RadioField("Status", choices=["Pending", "Published"])
    submit = SubmitField("Save")


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
        redis_client.set(f"recipe:{self.slug}", json.dumps(recipe))


def get_recipe_obj(slug) -> Recipe:
    recipe_str = redis_client.get(f"recipe:{slug}")
    r = json.loads(recipe_str)
    return Recipe(
        title=r.get("title"),
        slug=r.get("slug"),
        description=r.get("description"),
        ingredients=r.get("ingredients"),
        steps=r.get("steps"),
        tags=r.get("tags"),
        status=r.get("status"),  # TODO: smth
    )

def get_recipe_object(r) -> Recipe:
    status = PublishStatus.PENDING if r.get("status") == "Pending" else PublishStatus.PUBLISHED
    return Recipe(
        title=r.get("title"),
        slug=r.get("slug"),
        description=r.get("description"),
        ingredients=r.get("ingredients"),
        steps=r.get("steps"),
        tags=r.get("tags"),
        status=status
    )

def get_recipe_json(slug) -> dict:
    recipe_str = redis_client.get(f"recipe:{slug}")
    if not recipe_str:
        return {}
    return json.loads(recipe_str)

def get_all_recipes() -> List[Recipe]:
    _, keys = redis_client.scan(match="recipe:*")
    data = redis_client.mget(keys)
    res = []
    for d in data:
        r_dict = json.loads(d.decode("utf-8"))
        r = get_recipe_object(r_dict)
        res.append(r)
    return res


def get_recipe_slugs():
    _, keys = redis_client.scan(match="recipe:*")
    return [slug.decode("utf-8")[7:] for slug in keys]
