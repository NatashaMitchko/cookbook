from web.app import redis_client

from flask import Blueprint

recipe_bp = Blueprint("recipe_bp", __name__, template_folder="templates")


@recipe_bp.route("/")
def index():
    """
    Cookbook homepage
    """
    pass


@recipe_bp.route("/<slug>/")
def render_recipe(slug):
    recipe = redis_client.get(slug)
    return recipe
