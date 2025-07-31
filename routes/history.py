from flask import Blueprint, request, jsonify, render_template
from functions.history_func import load_history, save_history

history_bp = Blueprint("history", __name__)

@history_bp.route("/history", methods=["GET"])
def get_history():
    return jsonify(load_history())

@history_bp.route("/clear-history", methods=["POST"])
def clear_history():
    save_history([])
    return jsonify({"status": "History cleared"})

@history_bp.route("/view-history")
def view_history():
    return render_template("history.html")