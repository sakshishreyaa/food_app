import jwt
from functools import wraps
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from config import SECRET_KEY
from models import User
from app import db, redis_db


def authentication_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        # jwt is passed in the request header

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        # return 401 if token is not passed
        if not token:
            return jsonify({"status": "error", "message": "Token is missing !!"}), 401

        if redis_db.get(token):
            return (
                jsonify({"status": "error", "message": "Token is invalid login !!"}),
                401,
            )

        # decoding the payload to fetch the stored details
        data = decode_jwt(token)
        if data.get("status") == "error":
            return jsonify(data), 401

        # if token is not expired add to blacklisted tokens redis until expiration!
        if func.__name__ == "logout":
            # blacklist token ->redis with ttl as exp of token
            redis_db.set(token, data["pub_id"], ex=data["exp"])
            return (
                jsonify(
                    {"status": "success", "message": "Successfully logged out  !!"}
                ),
                200,
            )

        current_user = User.query.filter(User.phone == data["pub_id"][:10]).first()
        print(current_user, "current use", int(data["pub_id"][:10]))
        # returns the current logged in users context to the routes
        return func(current_user, *args, **kwargs)

    return wrapper


def generate_jwt(phone):
    token = jwt.encode(
        {"pub_id": str(phone) + "901", "exp": 129600000000000},  # 36 hours
        SECRET_KEY,
    )
    return token


def decode_jwt(token):
    try:
        return jwt.decode(token, SECRET_KEY, "HS256")
    except jwt.ExpiredSignatureError:
        return {
            "status": "error",
            "message": "Signature expired!!. Please log in again.",
        }
    except jwt.InvalidTokenError:
        return {"status": "error", "message": "Invalid token. Please log in again."}


def create_user(data):
    username = data.get("username")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
    if username and phone and password:
        user = User(
            name=username,
            email=email,
            phone=int(phone),
            password=generate_password_hash(password + SECRET_KEY),
        )
        db.session.add(user)
        db.session.commit()
        return {"status": "success", "message": "user created successfully"}

    else:
        return {
            "status": "error",
            "message": "missing inforformatio .provide username phone and password",
        }


def check_credentials(req_data, user):
    if check_password_hash(user.password, req_data["password"] + SECRET_KEY):
        return {"status": "success", "message": "login details verified successfully"}
    return {"status": "error", "message": " wrongg password "}


def get_user(login_id):
    print(db)
    print(User.query.all())
    print(type(login_id))
    print(
        User.query.filter(User.phone == login_id).one_or_none()
        if type(login_id) == int
        else User.query.filter(User.email == login_id).one_or_none(),
        "tttttttttt",
    )
    return (
        User.query.filter(User.phone == login_id).one_or_none()
        if login_id.isnumeric()
        else User.query.filter(User.email == login_id).one_or_none()
    )
