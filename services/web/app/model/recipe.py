from enum import Enum
from typing import List

from web.app import redis_client

class Status(Enum):
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
        status: Status,
    ) -> None:
        self.title = title
        self.slug = slug
        self.description = description
        self.ingredients = ingredients
        self.steps = steps
        self.tags = set(tags)
        self.status = status

    def save(self):
        json = {
            "title": self.title,
            "slug": self.slug,
            "description": self.description,
            "ingredients": self.ingredients,
            "steps": self.steps,
            "tags": list(self.tags),
            "status": self.status.name,
        }
        redis_client.set(self.slug, json)
