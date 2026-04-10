import logging
from flask import Blueprint, jsonify, request
from ext import db
from src.models.weather_record import WeatherRecord
from services import fetch_weather

logger = logging.getLogger(__name__)
api_bp = Blueprint("api", __name__)


@api_bp.route("/fetch-data", methods=["GET"])
def fetch_data():
    lat_str = request.args.get("lat")
    lon_str = request.args.get("lon")
    latitude = longitude = None

    if lat_str is not None or lon_str is not None:
        try:
            latitude  = float(lat_str)
            longitude = float(lon_str)
        except (TypeError, ValueError):
            return jsonify({"success": False, "error": "lat და lon რიცხვები უნდა იყოს."}), 400

        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            return jsonify({"success": False, "error": "lat [-90,90] და lon [-180,180] დიაპაზონში უნდა იყოს."}), 400

    try:
        weather_data = fetch_weather(latitude, longitude) if latitude else fetch_weather()
    except ConnectionError as exc:
        logger.warning("გარე API მიუწვდომელია: %s", exc)
        return jsonify({"success": False, "error": str(exc)}), 502
    except ValueError as exc:
        logger.warning("API-ს პასუხი არასწორია: %s", exc)
        return jsonify({"success": False, "error": str(exc)}), 502
    except Exception as exc:
        logger.exception("მოულოდნელი შეცდომა: %s", exc)
        return jsonify({"success": False, "error": "სერვერის შიდა შეცდომა."}), 500

    try:
        record = WeatherRecord(
            latitude=weather_data["latitude"],
            longitude=weather_data["longitude"],
            temperature=weather_data["temperature"],
            wind_speed=weather_data["wind_speed"],
            weather_code=weather_data["weather_code"],
        )
        record.save()
        logger.info("ჩანაწერი შენახულია: id=%s", record.id)
    except Exception as exc:
        db.session.rollback()
        logger.exception("ბაზაში შენახვა ვერ მოხდა: %s", exc)
        return jsonify({"success": False, "error": "ბაზაში შენახვა ვერ მოხდა."}), 500

    return jsonify({"success": True, "message": "მონაცემები შეინახა.", "data": record.to_dict()}), 200


@api_bp.route("/records", methods=["GET"])
def list_records():
    limit_str = request.args.get("limit", "50")

    try:
        limit = int(limit_str)
        if not (1 <= limit <= 500):
            raise ValueError
    except ValueError:
        return jsonify({"success": False, "error": "limit 1-დან 500-მდე უნდა იყოს."}), 400

    try:
        records = WeatherRecord.query.order_by(WeatherRecord.fetched_at.desc()).limit(limit).all()
    except Exception as exc:
        logger.exception("ჩანაწერების წაკითხვა ვერ მოხდა: %s", exc)
        return jsonify({"success": False, "error": "სერვერის შიდა შეცდომა."}), 500

    return jsonify({"success": True, "count": len(records), "data": [r.to_dict() for r in records]}), 200