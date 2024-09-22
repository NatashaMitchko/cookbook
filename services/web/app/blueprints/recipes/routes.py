from flask import Blueprint, render_template

from app.model.recipe import get_recipe, get_all_recipes

recipe_bp = Blueprint("recipe_bp", __name__, template_folder="templates")


@recipe_bp.route("/")
def homepage():
    """
    Cookbook homepage
    """
    recipes = get_all_recipes(published_only=True)
    return render_template("homepage.html", title="Natasha's Cookbook", recipes=recipes)
    


@recipe_bp.route("/<slug>/")
def render_recipe(slug):
    recipe = get_recipe(slug)
    return render_template("recipe.html", title=recipe.title, recipe=recipe)
