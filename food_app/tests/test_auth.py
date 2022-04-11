# import pytest
import sys
import requests

sys.path.extend(["/home/dell/my_projects/food_app/food_app", "/food_app"])
from auth.routes import *
from auth.utils import *

from app import db, redis_db


def test_register():
    response = requests.post(
        "http://localhost:5000/auth/register",
        json={
            "username": "saki",
            "email": "iuhj@ihj.nn",
            "phone": 97878,
            "password": "secret",
        },
    )
    print(response.content)
    user = get_user("97878")
    if user:
        print("-=============================")
    print(user)
    assert response.content == "success"
    assert response.status_code == 201


test_register()
# def test_host_routing_apple(client):
#     result = client.get("/", headers={"Host": "www.apple.com"})
#     assert b"This is the apple application." in result.data


# def test_host_routing_notfound(client):
#     result = client.get("/", headers={"Host": "www.notmango.com"})
#     assert b"Not Found" in result.data
#     assert 404 == result.status_code
