from flask import Blueprint, render_template

meta_bp = Blueprint("meta", __name__)

@meta_bp.route("/")
def index():
    return render_template("index.html")