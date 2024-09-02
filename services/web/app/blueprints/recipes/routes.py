from flask import Blueprint, render_template

from app.model.recipe import get_recipe

recipe_bp = Blueprint("recipe_bp", __name__, template_folder="templates")


@recipe_bp.route("/")
def index():
    """
    Cookbook homepage
    """
    pass


@recipe_bp.route("/<slug>/")
def render_recipe(slug):
    recipe = get_recipe(slug)
    return render_template("recipe.html", title=recipe.title, recipe=recipe)
