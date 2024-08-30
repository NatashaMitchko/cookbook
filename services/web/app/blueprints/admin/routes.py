from flask import Blueprint
from flask_login import login_required

admin_bp = Blueprint("admin_bp", __name__, template_folder="templates")


@admin_bp.route("/")
@login_required
def index():
    """
    Add new recipe button
    List with pending recipies for preview w/ preview and edit button
    List of published recipies w/ edit button
    Button to generate backup
    """
    pass


@admin_bp.route("/recipe")
@login_required
def recipe():
    pass


@admin_bp.route("/preview/<id>/")
@login_required
def preview_recipe(id):
    pass


@admin_bp.route("/backup")
@login_required
def generate_backup():
    pass
