from flask import Blueprint, request, jsonify
from functions.journal_func import view_journal, summarize_journal, get_dialogue_by_date, search_journal_by_keyword, extract_journal_tags

journal_bp = Blueprint("journal", __name__)

@journal_bp.route("/journal", methods=["GET"])
def journal_view():
    return jsonify(view_journal())

@journal_bp.route("/summarize-journal", methods=["GET"])
def summarize():
    return jsonify(summarize_journal())

@journal_bp.route("/recall-date", methods=["GET"])
def recall_date():
    date_str = request.args.get("date", "")
    result = get_dialogue_by_date(date_str)
    return jsonify({"date": date_str, "entries": result})

@journal_bp.route("/search-topic", methods=["GET"])
def search_topic():
    keyword = request.args.get("keyword", "")
    result = search_journal_by_keyword(keyword)
    return jsonify({"keyword": keyword, "matches": result})

@journal_bp.route("/journal-tags", methods=["GET"])
def journal_tags():
    tags = extract_journal_tags()
    return jsonify({"tags": tags})