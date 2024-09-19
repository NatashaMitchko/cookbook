from io import BytesIO
import os, json
from datetime import datetime
from typing import List

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    send_file,
    current_app,
    request,
)
from flask_login import login_required
from werkzeug.utils import secure_filename

import app.model.recipe as recipe
import app.utility.backup_restore as b

admin_bp = Blueprint("admin_bp", __name__, template_folder="templates")


@admin_bp.route("/")
def index():
    recipes = recipe.get_all_recipes()
    return render_template("admin_index.html", title="Admin Dashboard", recipes=recipes)


def remove_empties(input: List[str]) -> List[str]:
    result = []
    for x in input:
        if x == "":
            continue
        result.append(x)
    return result


@admin_bp.route("/recipe/new/", methods=["GET", "POST"])
@login_required
def new():
    form = recipe.RecipeForm()

    if form.add_ingredient.data:
        form.ingredients.append_entry(None)
    elif form.add_step.data:
        form.steps.append_entry(None)
    elif form.add_tag.data:
        form.tags.append_entry(None)

    elif form.validate_on_submit():
        r = recipe.Recipe(
            title=form.title.data,
            slug=form.slug.data,
            description=form.description.data,
            ingredients=remove_empties([i.data for i in form.ingredients]),
            steps=remove_empties([s.data for s in form.steps]),
            tags=remove_empties([t.data for t in form.tags]),
            status=(
                recipe.PublishStatus.PENDING
                if form.status.data == "Pending"
                else recipe.PublishStatus.PUBLISHED
            ),
        )
        r.save()
        return redirect(url_for("admin_bp.index"))
    return render_template("new_recipe.html", title="New Recipe", edit=False, form=form)


@admin_bp.route("/recipe/edit/<slug>/", methods=["GET", "POST"])
@login_required
def edit_recipe(slug):
    json_r = recipe.get_recipe_json(slug)
    json_r["status"] = json_r["status"].title()
    form = recipe.RecipeForm(data=json_r)

    if form.add_ingredient.data:
        form.ingredients.append_entry(None)
    elif form.add_step.data:
        form.steps.append_entry(None)
    elif form.add_tag.data:
        form.tags.append_entry(None)

    elif form.validate_on_submit():
        r = recipe.Recipe(
            title=form.title.data,
            slug=slug,
            description=form.description.data,
            ingredients=remove_empties([i.data for i in form.ingredients]),
            steps=remove_empties([s.data for s in form.steps]),
            tags=remove_empties([t.data for t in form.tags]),
            status=(
                recipe.PublishStatus.PENDING
                if form.status.data == "Pending"
                else recipe.PublishStatus.PUBLISHED
            ),
        )
        r.save()
        return redirect(url_for("admin_bp.index"))
    return render_template("new_recipe.html", title="Edit Recipe", edit=True, form=form)


@admin_bp.route("/backup", methods=["GET", "POST"])
@login_required
def backup():
    form = b.RecipeBackupFileForm()
    if form.validate_on_submit():
        f = form.backup.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(current_app.config["BACKUP_FOLDER"], filename))
        flash("Backup saved successfully.")
        if form.restore.data:
            fc = b.restore_from_backup(filename)
            flash(f"Restore Failure Count: {fc}")
        return redirect(url_for("admin_bp.index"))
    return render_template("bulk_upload.html", title="Backup", form=form)


@admin_bp.route("/bulk", methods=["POST"])
@login_required
def bulk():
    data = json.loads(request.data)
    slugs = data.get("slugs")
    action = data.get("action")
    if action == "tag":
        tag = data.get("tag")
        recipe.add_tag_to_recipes(tag, slugs)
        return {"status": 200}
    else:
        return {"action": "none"}  


@admin_bp.route("/download")
@login_required
def download():
    date = datetime.today().strftime("%Y-%m-%d")
    filename = f"{date}-recipe-download.json"
    recipes = recipe.get_all_json_recipies()
    byte_obj = BytesIO()
    for r in recipes:
        byte_obj.write(json.dumps(r).encode())
        byte_obj.write(b"\n")
    byte_obj.seek(0)
    return send_file(
        byte_obj,
        download_name=filename,
        mimetype="application/json",
        as_attachment=True,
    )


@admin_bp.route("/delete/<slug>")
@login_required
def delete(slug):
    recipe.delete_recipe(slug)


@admin_bp.route("/preview/<slug>/")
@login_required
def preview_recipe(slug):
    return recipe.get_recipe_json(slug)
