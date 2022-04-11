from flask import request, jsonify

from auth import auth
from auth.utils import (
    authentication_required,
    create_user,
    generate_jwt,
    get_user,
    check_credentials,
)


@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json(force=True)
    user = get_user(data["phone"])
    print(user, "popp")
    if user:
        print(user)
        return (
            jsonify(
                {"status": "error", "message": "User already exists,Please log in"}
            ),
            400,
        )

    try:
        resp = create_user(data)
        status_code = 400 if resp["status"] == "error" else 201
        return jsonify(resp), status_code
    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "unknown error occured .Exception :" + str(e),
                }
            ),
            500,
        )


@auth.route("/login", methods=["POST"])
def login():
    """
    Responsible for logging in user and creating jwt tokens for further auth

    Input : json data ->keys(phone/email(login_id ),password)
    """
    data = request.get_json(force=True)
    login_id = data.get("login_id")
    password = data.get("password")
    if not (login_id and password):
        return (
            jsonify(
                {"status": "error", "message": "Please provide login id and password"}
            ),
            400,
        )
    user = get_user(login_id)

    if not user:
        return (
            jsonify(
                {"status": "error", "message": "User doesn't exist,Pleaase register"}
            ),
            400,
        )

    try:
        login_resp = check_credentials(data, user)
        if login_resp["status"] == "error":
            return jsonify(login_resp), 401
        token = generate_jwt(user.phone)
        # TODO: add logic to store in session for now just return
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "user successfully logged in,log in token : ",
                    "data": token,
                }
            ),
            400,
        )
    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": "unknown error occured .Exception:" + e}
            ),
            500,
        )


@auth.route("/logout", methods=["POST"])
@authentication_required
def logout():

    """responsible for logging out user by blacklisting tokens"""
    return (
        jsonify({"status": "success", "message": "logged out!!"}),
        200,
    )
