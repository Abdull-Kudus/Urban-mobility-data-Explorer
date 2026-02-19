from flask import Blueprint, request, jsonify, current_app
from app.services.analytics_service import (
    get_hourly_demand,
    get_revenue_by_zone,
    get_avg_fare_per_distance,
    get_top_revenue_zones,
)

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/hourly-demand", methods=["GET"])
def hourly_demand():
    try:
        return jsonify({"data": get_hourly_demand()}), 200
    except Exception as e:
        current_app.logger.error(f"[/hourly-demand] {e}", exc_info=True)
        return jsonify({"error": "An internal server error occurred."}), 500


@analytics_bp.route("/revenue-by-zone", methods=["GET"])
def revenue_by_zone():
    try:
        return jsonify({"data": get_revenue_by_zone()}), 200
    except Exception as e:
        current_app.logger.error(f"[/revenue-by-zone] {e}", exc_info=True)
        return jsonify({"error": "An internal server error occurred."}), 500


@analytics_bp.route("/average-fare-per-mile", methods=["GET"])
def average_fare_per_mile():
    try:
        return jsonify({"data": get_avg_fare_per_distance()}), 200
    except Exception as e:
        current_app.logger.error(f"[/average-fare-per-mile] {e}", exc_info=True)
        return jsonify({"error": "An internal server error occurred."}), 500


@analytics_bp.route("/top-revenue-zones", methods=["GET"])
def top_revenue_zones():
    try:
        raw_n = request.args.get("n", "10")
        n = int(raw_n)
        if n < 1 or n > 50:
            return jsonify({"error": "Parameter 'n' must be between 1 and 50."}), 400
    except ValueError:
        return jsonify({"error": "Parameter 'n' must be an integer."}), 400

    try:
        data = get_top_revenue_zones(top_n=n)
        return jsonify({
            "algorithm": "merge_sort",
            "sorted_by": "total_revenue (descending)",
            "data":      data,
        }), 200
    except Exception as e:
        current_app.logger.error(f"[/top-revenue-zones] {e}", exc_info=True)
        return jsonify({"error": "An internal server error occurred."}), 500