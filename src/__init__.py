from flask import Flask, redirect, jsonify
import os
from src.auth import auth
from src.motorcyles import motorcycles
from src.database import db, Motorcycle
from src.constants.http_status_code import (
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from
from src.config.swagger import swagger_config, template
from src.config.config import config_dict

VERSION = 1.0


def create_app(config=config_dict["dev"]):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config)
    db.app = app
    db.init_app(app)

    JWTManager(app)
    app.register_blueprint(auth)
    app.register_blueprint(motorcycles)

    Swagger(app, config=swagger_config, template=template)

    @app.get("/<short_url>")
    @swag_from("./docs/short_url.yaml")
    def redirect_to_url(short_url):
        motorcycle = Motorcycle.query.filter(
            Motorcycle.short_url.ilike(short_url)
        ).first_or_404()

        if motorcycle:
            motorcycle.visits += 1
            db.session.commit()
            return redirect(motorcycle.url)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def page_not_found(e):
        return jsonify({"error": "Page not found"}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def internal_server_error(e):
        return (
            jsonify({"error": "Internal server error"}),
            HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return app
