from flask import Blueprint, request, redirect, url_for, flash, render_template, current_app
from werkzeug.utils import secure_filename
import os
import sys

from pipeline.hazard_pipeline import hazard_pipeline
from utils.geolocation import location_service
from utils.validator import validator
from logging.logging import logger
from exception.exception import CustomException

post_bp = Blueprint("posts", __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "frontend/static/uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@post_bp.route("/add", methods=["POST"])
def add_post():
    try:
        file = request.files.get("post")
        if not file:
            flash("No file uploaded")
            return redirect(url_for("home.home"))

        filename = secure_filename(file.filename)
        if not filename.lower().endswith((".jpg", ".jpeg", ".png", ".svg")):
            flash("Invalid image type")
            return redirect(url_for("home.home"))

        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        description = request.form["description"]
        location = request.form["location"]
        date = request.form["date"]
        time = request.form["time"]

        translated, cleaned, prediction, summary = hazard_pipeline.process(description)

        if prediction != 1:
            flash("Not a hazard description")
            return redirect(url_for("home.home"))

        is_india, lat, lon = location_service.get_location(location)
        if not is_india:
            flash("Location must be inside India")
            return redirect(url_for("home.home"))

        date = validator.validate_date(date)
        time = validator.validate_time(time)
        if not date or not time:
            flash("Invalid date/time")
            return redirect(url_for("home.home"))

        record = {
            "Post": filepath,
            "Description": cleaned,
            "Summary": summary,
            "Location": location,
            "Latitude": lat,
            "Longitude": lon,
            "Date": date.strftime("%Y-%m-%d"),
            "Time": time,
        }

        current_app.db.collection.insert_one(record)
        flash("Hazard post added.")
        return redirect(url_for("home.home"))

    except Exception as e:
        raise CustomException(e, sys)
