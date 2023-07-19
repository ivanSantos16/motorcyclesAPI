from flask import Blueprint, request, jsonify
import validators
from src.constants.http_status_code import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)
from src.database import Bookmark, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from flasgger import swag_from

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")


@bookmarks.route("/", methods=["POST", "GET"])
@jwt_required()
def handle_bookmarks():
    current_user = get_jwt_identity()
    if request.method == "POST":
        body = request.get_json().get("body", "")
        url = request.get_json().get("url", "")

        if not validators.url(url):
            return jsonify({"error": "Invalid URL"}), HTTP_400_BAD_REQUEST

        if Bookmark.query.filter_by(url=url).first() is not None:
            return jsonify({"error": "URL already exists"}), HTTP_409_CONFLICT

        bookmark = Bookmark(body=body, url=url, user_id=current_user)
        db.session.add(bookmark)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Bookmark created successfully",
                    "id": bookmark.id,
                    "url": bookmark.url,
                    "short_url": bookmark.short_url,
                    "visit_count": bookmark.visits,
                    "body": bookmark.body,
                    "created_at": bookmark.created_at,
                    "updated_at": bookmark.updated_at,
                }
            ),
            HTTP_201_CREATED,
        )

    else:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        bookmarks = Bookmark.query.filter_by(user_id=current_user).paginate(
            page=page, per_page=per_page
        )

        data = []

        for bookmark in bookmarks:
            data.append(
                {
                    "id": bookmark.id,
                    "url": bookmark.url,
                    "short_url": bookmark.short_url,
                    "visit_count": bookmark.visits,
                    "body": bookmark.body,
                    "created_at": bookmark.created_at,
                    "updated_at": bookmark.updated_at,
                }
            )

        meta = {
            "page": bookmarks.page,
            "pages": bookmarks.pages,
            "total_count": bookmarks.total,
            "prev_page": bookmarks.prev_num,
            "next_page": bookmarks.next_num,
            "has_next": bookmarks.has_next,
            "has_prev": bookmarks.has_prev,
        }

        return (
            jsonify(
                {
                    "message": "Bookmarks retrieved successfully",
                    "data": data,
                    "meta": meta,
                }
            ),
            HTTP_200_OK,
        )


@bookmarks.get("/<int:bookmark_id>")
@jwt_required()
def get_bookmark(bookmark_id):
    current_user = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(id=bookmark_id, user_id=current_user).first()

    if bookmark:
        return jsonify(
            {
                "message": "Bookmark retrieved successfully",
                "id": bookmark.id,
                "url": bookmark.url,
                "short_url": bookmark.short_url,
                "visit_count": bookmark.visits,
                "body": bookmark.body,
                "created_at": bookmark.created_at,
                "updated_at": bookmark.updated_at,
            },
            HTTP_200_OK,
        )
    return jsonify(
        {"error": "Bookmark not found"},
        HTTP_404_NOT_FOUND,
    )


@bookmarks.put("/<int:bookmark_id>")
@bookmarks.patch("/<int:bookmark_id>")
@jwt_required()
def update_bookmark(bookmark_id):
    current_user = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(id=bookmark_id, user_id=current_user).first()

    if bookmark:
        body = request.get_json().get("body", "")
        url = request.get_json().get("url", "")

        if not validators.url(url):
            return jsonify(
                {"error": "Invalid URL"},
                HTTP_400_BAD_REQUEST,
            )

        if Bookmark.query.filter_by(url=url).first() is not None:
            return jsonify(
                {"error": "URL already exists"},
                HTTP_409_CONFLICT,
            )

        bookmark.body = body
        bookmark.url = url
        bookmark.updated_at = datetime.now()
        db.session.commit()

        return jsonify(
            {
                "message": "Bookmark updated successfully",
                "id": bookmark.id,
                "url": bookmark.url,
                "short_url": bookmark.short_url,
                "visit_count": bookmark.visits,
                "body": bookmark.body,
                "created_at": bookmark.created_at,
                "updated_at": bookmark.updated_at,
            },
            HTTP_200_OK,
        )
    return jsonify(
        {"error": "Bookmark not found"},
        HTTP_404_NOT_FOUND,
    )


@bookmarks.delete("/<int:bookmark_id>")
@jwt_required()
def delete_bookmark(bookmark_id):
    current_user = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(id=bookmark_id, user_id=current_user).first()

    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()

        return jsonify(
            {},
            HTTP_204_NO_CONTENT,
        )
    return jsonify(
        {"error": "Bookmark not found"},
        HTTP_404_NOT_FOUND,
    )


@bookmarks.get("/stats")
@jwt_required()
@swag_from("./docs/bookmarks/stats.yaml")
def get_stats():
    current_user = get_jwt_identity()
    bookmarks = Bookmark.query.filter_by(user_id=current_user).all()

    data = []

    for bookmark in bookmarks:
        new_link = {
            "visits": bookmark.visits,
            "url": bookmark.url,
            "id": bookmark.id,
            "short_url": bookmark.short_url,
        }

        data.append(new_link)

    return jsonify(
        {
            "message": "Bookmarks retrieved successfully",
            "data": data,
        },
        HTTP_200_OK,
    )
