from datetime import datetime, timedelta

from sqlalchemy.sql.expression import true, update
from sqlalchemy.sql.functions import user

from models import Booking, Restaurant


class BookingUtility:
    @staticmethod
    def get_bookings(data):
        restaurant_id = data.get("restaurant_id")
        if not restaurant_id:
            {"status": "error", "message": "insufficient input provide "}, 400
        else:
            return (
                Booking.query.filter(Booking.restaurant_id == restaurant_id).all(),
                200,
            )

    @staticmethod
    def get_my_bookings(data):
        user_id = data.get("user_id")
        if not user_id:
            {"status": "error", "message": "insufficient input provide "}, 400
        else:
            return (
                Booking.query.filter(Booking.user_id == user_id).all(),
                200,
            )

    @staticmethod
    def seats_available(from_time, to_time, restaurant_id, no_of_guests):
        return (
            True
            if Booking.get_available_seats(
                from_time=from_time, to_time=to_time, restaurant_id=restaurant_id
            )
            >= no_of_guests
            else False
        )

    @staticmethod
    def create_booking(data):
        restaurant_id = data.get("restaurant_id")
        date = data.get("date")
        hours = data.get("hours")
        from_time = datetime.strptime(
            date.strip() + " " + data.get("from").strip(), "%b %d %Y %I:%M"
        )
        to_time = from_time + timedelta(hours=hours)
        no_of_guests = data.get("no_of_guests")
        user_id = data.get("user_id")
        if not all(
            (restaurant_id, date, user_id, hours, from_time, to_time, no_of_guests)
        ):
            return {"status": "error", "message": "insufficient input provide "}, 400
        elif not BookingUtility.seats_available(
            from_time, to_time, restaurant_id, no_of_guests
        ):
            return {"status": "error", "message": "seats not available"}, 200
        else:
            Booking(
                restaurant_id=restaurant_id,
                from_time=from_time,
                to_time=to_time,
                no_of_guests=no_of_guests,
                user_id=user_id,
            )
            return {"status": "success", "message": "successfully created booking"}, 201

    @staticmethod
    def cancel_booking(data):
        booking_id = data.get("booking_id")
        if not BookingUtility.validate_input(booking_id):
            {"status": "error", "message": "insufficient input provide "}, 400
        else:
            return (
                Booking.query.filter(Booking.id == booking_id).delete(),
                200,
            )

    @staticmethod
    def update_booking(data):
        booking_id = data.get("booking_id")
        updated_no_guests = data.get("updated_no_guests")
        date = data.get("date")
        hours = data.get("hours")
        from_time = datetime.strptime(
            date.strip() + " " + data.get("from").strip(), "%b %d %Y %I:%M"
        )
        to_time = from_time + timedelta(hours=hours)
        no_of_guests = data.get("no_of_guests")
        restaurant_id = data.get("restaurant_id")
        if not all(
            (booking_id, from_time, to_time, no_of_guests, restaurant_id, booking_id)
        ):
            {"status": "error", "message": "insufficient input provide "}, 400
        elif updated_no_guests > no_of_guests and not BookingUtility.seats_available(
            from_time, to_time, restaurant_id, updated_no_guests - no_of_guests
        ):
            return {"status": "error", "message": "seats not available"}, 200
        else:
            Booking.query.filter(Booking.id == booking_id).update(
                {
                    "no_of_guests": updated_no_guests or no_of_guests,
                    "from_time": from_time,
                    "to_time": to_time,
                }
            ),
            return {"status": "success", "message": "successfully updated bookimg"}, 200
