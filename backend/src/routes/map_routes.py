from flask import Blueprint, render_template, jsonify, current_app

map_bp = Blueprint("map", __name__)

@map_bp.route("/map")
def show_map():
    return render_template("map.html")

@map_bp.route("/map_data")
def map_data():
    posts = list(current_app.db.collection.find({}, {"_id": 0}))
    for post in posts:
        post["Latitude"] = float(post["Latitude"])
        post["Longitude"] = float(post["Longitude"])
    return jsonify(posts)
