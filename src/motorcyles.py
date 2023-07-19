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
from src.database import Motorcycle, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from flasgger import swag_from

motorcycles = Blueprint("motorcycles", __name__, url_prefix="/api/v1/motorcycles")


@motorcycles.route("/", methods=["POST", "GET"])
@jwt_required()
@swag_from("./docs/motorcycles/search.yaml", methods=["GET"])
@swag_from("./docs/motorcycles/post.yaml", methods=["POST"])
def handle_motorcycles():
    current_user = get_jwt_identity()

    match request.method:
        case "POST":
            r = request.get_json()
            parameters = dict()

            for param in [
                "niv",
                "brand",
                "model",
                "year",
                "category",
                "rating",
                "displacement",
                "power",
                "torque",
                "engine_cylinders",
                "engine_stroke",
                "gearbox",
                "bore",
                "stroke",
                "transmission_type",
                "front_brakes",
                "rear_brakes",
                "front_suspension",
                "rear_suspension",
                "front_tire",
                "rear_tire",
                "dry_weight",
                "wheelbase",
                "fuel_capacity",
                "fuel_system",
                "fuel_control",
                "seat_height",
                "cooling_system",
                "color_options",
                "url",
            ]:
                if param not in r:
                    return (
                        jsonify({"error": f"Missing {param} parameter"}),
                        HTTP_400_BAD_REQUEST,
                    )

                parameters[param] = r.get(param, "")

            parameters["url"] = request.get_json().get("url", "")

            if not validators.url(parameters["url"]):
                return jsonify({"error": "Invalid URL"}), HTTP_400_BAD_REQUEST

            if (
                Motorcycle.query.filter(Motorcycle.url.ilike(parameters["url"])).first()
                is not None
            ):
                return jsonify({"error": "URL already exists"}), HTTP_409_CONFLICT

            if (
                Motorcycle.query.filter(Motorcycle.niv.ilike(parameters["niv"])).first()
                is not None
            ):
                return jsonify({"error": "NIV already exists"}), HTTP_409_CONFLICT

            motorcycle = Motorcycle(
                niv=parameters["niv"],
                brand=parameters["brand"],
                model=parameters["model"],
                year=parameters["year"],
                category=parameters["category"],
                rating=parameters["rating"],
                displacement=parameters["displacement"],
                power=parameters["power"],
                torque=parameters["torque"],
                engine_cylinders=parameters["engine_cylinders"],
                engine_stroke=parameters["engine_stroke"],
                gearbox=parameters["gearbox"],
                bore=parameters["bore"],
                stroke=parameters["stroke"],
                transmission_type=parameters["transmission_type"],
                front_brakes=parameters["front_brakes"],
                rear_brakes=parameters["rear_brakes"],
                front_suspension=parameters["front_suspension"],
                rear_suspension=parameters["rear_suspension"],
                front_tire=parameters["front_tire"],
                rear_tire=parameters["rear_tire"],
                dry_weight=parameters["dry_weight"],
                wheelbase=parameters["wheelbase"],
                fuel_capacity=parameters["fuel_capacity"],
                fuel_system=parameters["fuel_system"],
                fuel_control=parameters["fuel_control"],
                seat_height=parameters["seat_height"],
                cooling_system=parameters["cooling_system"],
                color_options=parameters["color_options"],
                url=parameters["url"],
                user_id=current_user,
            )
            db.session.add(motorcycle)
            db.session.commit()

            return (
                jsonify(
                    {
                        "message": f"Motorcycle {motorcycle.niv} added successfully",
                        "niv": motorcycle.niv,
                        "brand": motorcycle.brand,
                        "model": motorcycle.model,
                        "year": motorcycle.year,
                        "url": motorcycle.url,
                        "short_url": motorcycle.short_url,
                        "visit_count": motorcycle.visits,
                    }
                ),
                HTTP_201_CREATED,
            )

        case "GET":
            page = request.args.get("page", 1, type=int)
            per_page = request.args.get("per_page", 10, type=int)

            match len(request.args):
                case 0:
                    motorcycles = Motorcycle.query.paginate(
                        page=page, per_page=per_page
                    )

                    data = []

                    for motorcycle in motorcycles:
                        data.append(
                            {
                                "niv": motorcycle.niv,
                                "brand": motorcycle.brand,
                                "model": motorcycle.model,
                                "year": motorcycle.year,
                                "category": motorcycle.category,
                                "rating": motorcycle.rating,
                                "displacement": motorcycle.displacement,
                                "power": motorcycle.power,
                                "torque": motorcycle.torque,
                                "engine_cylinders": motorcycle.engine_cylinders,
                                "engine_stroke": motorcycle.engine_stroke,
                                "gearbox": motorcycle.gearbox,
                                "bore": motorcycle.bore,
                                "stroke": motorcycle.stroke,
                                "transmission_type": motorcycle.transmission_type,
                                "front_brakes": motorcycle.front_brakes,
                                "rear_brakes": motorcycle.rear_brakes,
                                "front_suspension": motorcycle.front_suspension,
                                "rear_suspension": motorcycle.rear_suspension,
                                "dry_weight": motorcycle.dry_weight,
                                "wheelbase": motorcycle.wheelbase,
                                "fuel_capacity": motorcycle.fuel_capacity,
                                "fuel_system": motorcycle.fuel_system,
                                "fuel_control": motorcycle.fuel_control,
                                "seat_height": motorcycle.seat_height,
                                "cooling_system": motorcycle.cooling_system,
                                "color_options": motorcycle.color_options,
                                "url": motorcycle.url,
                                "short_url": motorcycle.short_url,
                                "visit_count": motorcycle.visits,
                                "created_at": motorcycle.created_at,
                                "updated_at": motorcycle.updated_at,
                            }
                        )

                    meta = {
                        "page": motorcycles.page,
                        "pages": motorcycles.pages,
                        "total_count": motorcycles.total,
                        "prev_page": motorcycles.prev_num,
                        "next_page": motorcycles.next_num,
                        "has_next": motorcycles.has_next,
                        "has_prev": motorcycles.has_prev,
                    }

                    return (
                        jsonify(
                            {
                                "message": "Motorcycles retrieved successfully",
                                "data": data,
                                "meta": meta,
                            }
                        ),
                        HTTP_200_OK,
                    )

                case _:
                    data = []

                    query = Motorcycle.query

                    for key in request.args.keys():
                        if key not in [
                            "brand",
                            "model",
                            "year",
                            "category",
                            "per_page",
                            "page",
                        ]:
                            return (
                                jsonify(
                                    {
                                        "error": f"Invalid parameter - {key}"
                                    }
                                ),
                                HTTP_400_BAD_REQUEST,
                            )

                    if "brand" in request.args.keys():
                        query = query.filter(
                            Motorcycle.brand.ilike(request.args["brand"])
                        )

                    if "model" in request.args.keys():
                        query = query.filter(
                            Motorcycle.model.ilike(request.args["model"])
                        )

                    if "year" in request.args.keys():
                        query = query.filter(
                            Motorcycle.year.ilike(request.args["year"])
                        )

                    if "category" in request.args.keys():
                        query = query.filter(
                            Motorcycle.category.ilike(request.args["category"])
                        )

                    motorcycles = query.paginate(page=page, per_page=per_page)

                    match len(motorcycles.items):
                        case 0:
                            return (
                                jsonify({"error": "No motorcycles found"}),
                                HTTP_404_NOT_FOUND,
                            )

                        case _:
                            for motorcycle in motorcycles:
                                data.append(
                                    {
                                        "niv": motorcycle.niv,
                                        "brand": motorcycle.brand,
                                        "model": motorcycle.model,
                                        "year": motorcycle.year,
                                        "category": motorcycle.category,
                                        "rating": motorcycle.rating,
                                        "displacement": motorcycle.displacement,
                                        "power": motorcycle.power,
                                        "torque": motorcycle.torque,
                                        "engine_cylinders": motorcycle.engine_cylinders,
                                        "engine_stroke": motorcycle.engine_stroke,
                                        "gearbox": motorcycle.gearbox,
                                        "bore": motorcycle.bore,
                                        "stroke": motorcycle.stroke,
                                        "transmission_type": motorcycle.transmission_type,
                                        "front_brakes": motorcycle.front_brakes,
                                        "rear_brakes": motorcycle.rear_brakes,
                                        "front_suspension": motorcycle.front_suspension,
                                        "rear_suspension": motorcycle.rear_suspension,
                                        "front_tire": motorcycle.front_tire,
                                        "rear_tire": motorcycle.rear_tire,
                                        "dry_weight": motorcycle.dry_weight,
                                        "wheelbase": motorcycle.wheelbase,
                                        "fuel_capacity": motorcycle.fuel_capacity,
                                        "fuel_system": motorcycle.fuel_system,
                                        "fuel_control": motorcycle.fuel_control,
                                        "seat_height": motorcycle.seat_height,
                                        "cooling_system": motorcycle.cooling_system,
                                        "color_options": motorcycle.color_options,
                                        "url": motorcycle.url,
                                        "short_url": motorcycle.short_url,
                                        "visit_count": motorcycle.visits,
                                        "created_at": motorcycle.created_at,
                                        "updated_at": motorcycle.updated_at,
                                    }
                                )

                            meta = {
                                "page": motorcycles.page,
                                "pages": motorcycles.pages,
                                "total_count": motorcycles.total,
                                "prev_page": motorcycles.prev_num,
                                "next_page": motorcycles.next_num,
                                "has_next": motorcycles.has_next,
                                "has_prev": motorcycles.has_prev,
                            }

                            return (
                                jsonify(
                                    {
                                        "message": "Motorcycles retrieved successfully",
                                        "data": data,
                                        "meta": meta,
                                    }
                                ),
                                HTTP_200_OK,
                            )


@motorcycles.get("/<string:motorcycles_niv>")
@jwt_required()
@swag_from("./docs/motorcycles/get.yaml")
def get_motorcycles(motorcycles_niv):
    current_user = get_jwt_identity()
    motorcycle = Motorcycle.query.filter(Motorcycle.niv.ilike(motorcycles_niv)).first()

    if motorcycle:
        return (
            jsonify(
                {
                    "message": "Motorcycle retrieved successfully",
                    "data": {
                        "niv": motorcycle.niv,
                        "brand": motorcycle.brand,
                        "model": motorcycle.model,
                        "year": motorcycle.year,
                        "category": motorcycle.category,
                        "rating": motorcycle.rating,
                        "displacement": motorcycle.displacement,
                        "power": motorcycle.power,
                        "torque": motorcycle.torque,
                        "engine_cylinders": motorcycle.engine_cylinders,
                        "engine_stroke": motorcycle.engine_stroke,
                        "gearbox": motorcycle.gearbox,
                        "bore": motorcycle.bore,
                        "stroke": motorcycle.stroke,
                        "transmission_type": motorcycle.transmission_type,
                        "front_brakes": motorcycle.front_brakes,
                        "rear_brakes": motorcycle.rear_brakes,
                        "front_suspension": motorcycle.front_suspension,
                        "rear_suspension": motorcycle.rear_suspension,
                        "front_tire": motorcycle.front_tire,
                        "rear_tire": motorcycle.rear_tire,
                        "dry_weight": motorcycle.dry_weight,
                        "wheelbase": motorcycle.wheelbase,
                        "fuel_capacity": motorcycle.fuel_capacity,
                        "fuel_system": motorcycle.fuel_system,
                        "fuel_control": motorcycle.fuel_control,
                        "seat_height": motorcycle.seat_height,
                        "cooling_system": motorcycle.cooling_system,
                        "color_options": motorcycle.color_options,
                        "url": motorcycle.url,
                        "short_url": motorcycle.short_url,
                        "visit_count": motorcycle.visits,
                        "created_at": motorcycle.created_at,
                        "updated_at": motorcycle.updated_at,
                    },
                }
            ),
            HTTP_200_OK,
        )

    return jsonify({"error": "Motorcycle not found"}), HTTP_404_NOT_FOUND


@motorcycles.put("/<string:motorcycles_niv>")
@motorcycles.patch("/<string:motorcycles_niv>")
@jwt_required()
@swag_from("./docs/motorcycles/update.yaml")
def update_motorcycle(motorcycles_niv):
    print(motorcycles_niv)
    current_user = get_jwt_identity()
    motorcycle = Motorcycle.query.filter(Motorcycle.niv.ilike(motorcycles_niv)).first()

    available_parameters = [
        "niv",
        "brand",
        "model",
        "year",
        "category",
        "rating",
        "displacement",
        "power",
        "torque",
        "engine_cylinders",
        "engine_stroke",
        "gearbox",
        "bore",
        "stroke",
        "transmission_type",
        "front_brakes",
        "rear_brakes",
        "front_suspension",
        "rear_suspension",
        "front_tire",
        "rear_tire",
        "dry_weight",
        "wheelbase",
        "fuel_capacity",
        "fuel_system",
        "fuel_control",
        "seat_height",
        "cooling_system",
        "color_options",
        "url",
    ]

    if motorcycle:
        # Get all the data from the request to create a new motorcycle
        if url:= request.json.get("url", None):

            if not validators.url(url):
                return jsonify(
                    {"error": "Invalid parameter - {url}"}), HTTP_400_BAD_REQUEST
                

            if Motorcycle.query.filter_by(url=url).first() is not None:
                return jsonify(
                    {"error": "URL already exists"}), HTTP_409_CONFLICT
            
        for key in request.json:
            if key not in available_parameters:
                return jsonify(
                    {"error": f"Invalid parameter - {key}"}), HTTP_400_BAD_REQUEST
                
            else:
                setattr(motorcycle, key, request.json.get(key))

        motorcycle.updated_at = datetime.now()
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Motorcycle updated successfully",
                    "data": {
                        "niv": motorcycle.niv,
                        "brand": motorcycle.brand,
                        "model": motorcycle.model,
                        "year": motorcycle.year,
                        "url": motorcycle.url,
                        "short_url": motorcycle.short_url,
                        "visit_count": motorcycle.visits,
                        "created_at": motorcycle.created_at,
                        "updated_at": motorcycle.updated_at,
                    },
                }
            ),
            HTTP_200_OK,
        )

    return jsonify(
        {"error": f"Motorcycle with NIV - {motorcycles_niv} - not found"}), HTTP_404_NOT_FOUND
    


@motorcycles.delete("/<string:motorcycles_niv>")
@jwt_required()
@swag_from("./docs/motorcycles/delete.yaml")
def delete_motorcycle(motorcycles_niv):
    current_user = get_jwt_identity()
    motorcycle = Motorcycle.query.filter(Motorcycle.niv.ilike(motorcycles_niv)).first()

    if motorcycle:
        db.session.delete(motorcycle)
        db.session.commit()

        return jsonify({}), HTTP_204_NO_CONTENT

    return (
        jsonify({"error": f"Motorcycle with niv - {motorcycles_niv} - not found"}),
        HTTP_404_NOT_FOUND,
    )


@motorcycles.get("/stats")
@jwt_required()
@swag_from("./docs/motorcycles/stats.yaml")
def get_stats():
    current_user = get_jwt_identity()
    motorcycles = Motorcycle.query.filter(Motorcycle.user_id.ilike(current_user)).all()

    data = []

    for motorcycle in motorcycles:
        new_link = {
            "visits": motorcycle.visits,
            "url": motorcycle.url,
            "niv": motorcycle.niv,
            "short_url": motorcycle.short_url,
        }

        data.append(new_link)

    return (
        jsonify(
            {
                "message": "Motorcycles related to user retrieved successfully",
                "data": data,
            }
        ),
        HTTP_200_OK,
    )
