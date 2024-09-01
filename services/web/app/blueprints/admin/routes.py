import json

from flask import Blueprint, render_template, redirect, url_for

# from flask_login import login_required
from app import redis_client
from app.model.recipe import RecipeForm, Recipe, PublishStatus

admin_bp = Blueprint("admin_bp", __name__, template_folder="templates")


@admin_bp.route("/")
# @login_required
def index():
    """
    Add new recipe button
    List with pending recipies for preview w/ preview and edit button
    List of published recipies w/ edit button
    Button to generate backup
    """
    pass


@admin_bp.route("/recipe/new/", methods=["GET", "POST"])
# @login_required
def recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        r = Recipe(
            title=form.title.data,
            slug=form.slug.data,
            description=form.description.data,
            ingredients=[i.data for i in form.ingredients],
            steps=[s.data for s in form.steps],
            tags=[t.data for t in form.tags],
            status=(
                PublishStatus.PENDING
                if form.status.data == "Pending"
                else PublishStatus.PUBLISHED
            ),
        )
        r.save()
        return redirect(url_for("admin_bp.preview_recipe", slug=r.slug))
    return render_template("new_recipe.html", title="New Recipe", form=form)


@admin_bp.route("/recipe/edit/<slug>/", methods=["GET", "POST"])
def edit_recipe(slug):
    recipe = redis_client.get(slug)
    json_r = json.loads(recipe)
    form = RecipeForm(data=json_r)
    if form.validate_on_submit():
        r = Recipe(
            title=form.title.data,
            slug=slug,
            description=form.description.data,
            ingredients=[i.data for i in form.ingredients],
            steps=[s.data for s in form.steps],
            tags=[t.data for t in form.tags],
            status=(
                PublishStatus.PENDING
                if form.status.data == "Pending"
                else PublishStatus.PUBLISHED
            ),
        )
        r.save()
        return redirect(url_for("admin_bp.preview_recipe", slug=r.slug))
    return render_template("edit_recipe.html", title="Edit Recipe", form=form)


@admin_bp.route("/preview/<slug>/")
# @login_required
def preview_recipe(slug):
    recipe = redis_client.get(slug)
    r = json.loads(recipe)
    return r


@admin_bp.route("/backup/")
# @login_required
def generate_backup():
    pass
