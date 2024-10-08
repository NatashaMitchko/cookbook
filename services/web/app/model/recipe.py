from enum import Enum
from typing import List
import json
import re

from app import redis_client

class PublishStatus(Enum):
    PENDING = 1
    PUBLISHED = 2

def is_valid_slug(s: str) -> bool:
    if re.search("^[a-zA-Z]+(-?[a-zA-Z]+)*$", s):
        return True
    return False

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
        self.title = title.title()
        self.slug = slug
        self.description = description
        self.ingredients = ingredients
        self.steps = steps
        self.tags = set(tags)
        self.status = status

    def save(self):
        recipe = {
            "title": self.title.title(),
            "slug": self.slug,
            "description": self.description,
            "ingredients": self.ingredients,
            "steps": self.steps,
            "tags": list(self.tags),
            "status": self.status.name,
        }
        redis_client.set(f"recipe:{self.slug}", json.dumps(recipe))

def get_recipe(slug) -> Recipe:
    r_json = get_recipe_json(slug)
    return get_recipe_object(r_json)

def get_recipe_object(r) -> Recipe:
    status = PublishStatus.PENDING if r.get("status") == "PENDING" else PublishStatus.PUBLISHED
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

def get_all_recipes(published_only=False) -> List[Recipe]:
    res = []
    for key in redis_client.scan_iter(match="recipe:*"):
        data = redis_client.get(key)
        r_dict = json.loads(data.decode("utf-8"))

        r = get_recipe_object(r_dict)
        if published_only and r.status == PublishStatus.PUBLISHED:
            res.append(r)
        elif not published_only:
            res.append(r)

    return res

def get_all_json_recipies() -> str:
    res = []
    for key in redis_client.scan_iter(match="recipe:*"):
        data = redis_client.get(key)
        r_dict = json.loads(data.decode("utf-8"))
        res.append(r_dict)
    return res

def delete_recipe(slug) -> bool:
    redis_client.delete(f"recipe:{slug}")

def add_tag_to_recipes(tag, slugs):
    for slug in slugs:
        r = get_recipe(slug)
        r.tags.add(tag)
        r.save()
