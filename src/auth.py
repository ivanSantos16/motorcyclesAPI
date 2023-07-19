from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from src.constants.http_status_code import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
    HTTP_201_CREATED,
    HTTP_200_OK,
)
import validators
from src.database import User, db
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
)
from flasgger import swag_from

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post("/register")
@swag_from("./docs/auth/register.yaml")
def register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    SpecialSym = ["$", "@", "#", "%", "!", "*"]

    if len(password) < 8:
        return (
            jsonify({"error": "Password must be at least 8 characters long"}),
            HTTP_400_BAD_REQUEST,
        )

    if not any(char.isdigit() for char in password):
        return (
            jsonify({"error": "Password should have at least one numeral"}),
            HTTP_400_BAD_REQUEST,
        )

    if not any(char.isupper() for char in password):
        return (
            jsonify({"error": "Password should have at least one uppercase letter"}),
            HTTP_400_BAD_REQUEST,
        )

    if not any(char.islower() for char in password):
        return (
            jsonify({"error": "Password should have at least one lowercase letter"}),
            HTTP_400_BAD_REQUEST,
        )

    if not any(char in SpecialSym for char in password):
        return (
            jsonify(
                {"error": "Password should have at least one of the symbols $@#%!*"}
            ),
            HTTP_400_BAD_REQUEST,
        )

    if len(username) < 3:
        return (
            jsonify({"error": "Username must be at least 3 characters long"}),
            HTTP_400_BAD_REQUEST,
        )

    if not username.isalnum() or " " in username:
        return (
            jsonify({"error": "Username must be alphanumeric and not contain spaces"}),
            HTTP_400_BAD_REQUEST,
        )

    if not validators.email(email):
        return jsonify({"error": "Invalid email address"}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email address already in use"}), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "Username already in use"}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user = User(username=username, email=email, password=pwd_hash)
    db.session.add(user)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "User created successfully",
                "user": {
                    "username": user.username,
                    "email": user.email,
                },
            }
        ),
        HTTP_201_CREATED,
    )


@auth.post("/login")
@swag_from("./docs/auth/login.yaml")
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    user = User.query.filter_by(email=email).first()

    if user:
        is_password_correct = check_password_hash(user.password, password)

        if is_password_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return (
                jsonify(
                    {
                        "message": "User logged in successfully",
                        "user": {
                            "username": user.username,
                            "email": user.email,
                            "refresh": refresh,
                            "access": access,
                        },
                    }
                ),
                HTTP_200_OK,
            )

        return jsonify({"error": "Wrong credentials"}), HTTP_401_UNAUTHORIZED
    return jsonify({"error": "Wrong credentials"}), HTTP_401_UNAUTHORIZED


@auth.get("/me")
@jwt_required()
@swag_from("./docs/auth/me.yaml")
def me():
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()

    return (
        jsonify(
            {
                "message": "User retrieved successfully",
                "user": {
                    "username": user.username,
                    "email": user.email,
                },
            }
        ),
        HTTP_200_OK,
    )


@auth.get("/token/refresh")
@jwt_required(refresh=True)
@swag_from("./docs/auth/refresh_token.yaml")
def refresh_user_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)
    return (
        jsonify(
            {
                "message": "Token refreshed successfully",
                "access": access,
            }
        ),
        HTTP_200_OK,
    )
