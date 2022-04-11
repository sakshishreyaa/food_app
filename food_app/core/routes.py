from flask import jsonify, request
from datetime import datetime, timedelta

from core import core
from core.utils import BookingUtility
from models import Restaurant, User, Booking
from auth.utils import authentication_required


@core.route("/get_bookings", methods=["GET"])
def get_bookings():
    """
    Args :
        restaurant_id : id of restauerat id to get bookings
    """
    try:

        data = request.get_json(force=True)
        response, status_code = BookingUtility.get_bookings(data)
        return jsonify(response), status_code

    except Exception as e:
        print(e.__traceback__())
        return jsonify({"message": "some error occured"}), 400


@core.route("/get_my_bookings", methods=["POST"])
@authentication_required
def get_my_bookings(user: User):
    """
    Args:
        user_id: user_id (implicit )
    """
    try:

        data = {"user_id": user.id}
        response, status_code = BookingUtility.get_bookings(data)
        return jsonify(response), status_code

    except:
        print(Exception.__traceback__())
        return jsonify({"message": "some error occured"}), 400


@core.route("/create_booking", methods=["POST"])
@authentication_required
def create_booking(user: User):
    """
    Args:
        restaurant_id:
        date:
        from:
        hours:
        no_of_guests:
        user_id:(implicit)
    """
    try:
        data = request.get_json(force=True)
        data.update({"user_id": user.id})
        response, status_code = BookingUtility.create_booking(data)
        return jsonify(response), status_code

    except:
        print(Exception.__traceback__())
        return jsonify({"message": "some error occured"}), 400


@core.route("/cancel_booking", methods=["POST"])
@authentication_required
def cancel_booking(user: User):
    """
    Args:
        booking_id:
    """
    try:
        data = request.get_json(force=True)
        response, status_code = BookingUtility.cancel_booking(data)
        return jsonify(response), status_code

    except:
        print(Exception.__traceback__())
        return jsonify({"message": "some error occured"}), 400


@core.route("/update_booking", methods=["PATCH"])
@authentication_required
def update_booking(user: User):
    """
    Args:
        booking_id:
        old_no_of_guests
        new_no_of_guests:
        from_time:
        hours:
        restaurant_id
    """
    try:
        data = request.get_json(force=True)
        response, status_code = BookingUtility.update_booking(data)
        return jsonify(response), status_code

    except:
        print(Exception.__traceback__())
        return jsonify({"message": "some error occured"}), 400
