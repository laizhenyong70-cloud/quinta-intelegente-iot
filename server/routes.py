from flask import Blueprint, jsonify
from database import get_latest_data,get_history_data
api_bp = Blueprint("api",__name__)

@api_bp.route("/api/data/latest",methods=["GET"])
def latest_data():
    data = get_latest_data()
    if data is None:
        return jsonify({"message":"No data found"}),404
    else:
        return jsonify(data)

@api_bp.route("/api/data/history",methods=["GET"])
def history_data():
    data = get_history_data()
    return jsonify(data)
