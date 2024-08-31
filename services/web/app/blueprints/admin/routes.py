from flask import Blueprint, request, render_template
# from flask_login import login_required

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
    if request.method == "GET":
        return render_template("new_recipe.html", title="New Recipe")
    else:
        # do WTF forms
        return "hello"

@admin_bp.route("/preview/<id>/")
# @login_required
def preview_recipe(id):
    pass


@admin_bp.route("/backup/")
# @login_required
def generate_backup():
    pass
