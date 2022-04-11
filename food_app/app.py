import os
import redis
from flask.json import jsonify
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import *

app = Flask(__name__)


DATABASE_CONNECTION_URI = (
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
)
print(
    DATABASE_CONNECTION_URI,
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
redis_db = redis.Redis(host="0.0.0.0")
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def register_root_route():
    @app.route("/")
    def hello():
        output = []
        for rule in app.url_map.iter_rules():

            options = {}
            for arg in rule.arguments:
                options[arg] = "[{0}]".format(arg)

            methods = ",".join(rule.methods)
            url = url_for(rule.endpoint, **options)
            line = "{:50s} {:20s} {}".format(rule.endpoint, methods, url)
            output.append(line)
        return jsonify({"message": output}), 200


def create_app():

    from core import core, routes
    from auth import auth, routes
    from models import init_db

    register_root_route()
    app.register_blueprint(core)
    app.register_blueprint(auth)
    init_db()
    app.run(debug=True, host="localhost")


if __name__ == "__main__":
    create_app()
