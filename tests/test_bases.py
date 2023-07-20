import unittest
import os
from src.config.config import config_dict
from src import create_app
from src.database import db, Motorcycle, User


class UserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(config=config_dict["testing"])
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self) -> None:
        db.drop_all()
        self.app_context.pop()
        self.app = None
        self.client = None

    def test_create_user_for_model(self):
        user = User(username="test", email="test@email.com", password="Test123!")
        self.assertEqual(user.username, "test")
        self.assertEqual(user.email, "test@email.com")
        self.assertEqual(user.__repr__(), f"User>>> {user.username}")

    def test_create_motorcycle_for_model(self):
        motorcycle = Motorcycle(
            niv="12345678901234567",
            brand="test",
            model="test",
            year=2021,
            category="test",
            rating=5.0,
            displacement=1000,
            power=100.0,
            torque=100,
            engine_cylinders="test",
            engine_stroke="test",
            gearbox="test",
            bore=100,
            stroke=100.0,
            transmission_type="test",
            front_brakes="test",
            rear_brakes="test",
            front_suspension="test",
            rear_suspension="test",
            front_tire="test",
            rear_tire="test",
            dry_weight=1000,
            wheelbase=1000,
            fuel_capacity=1000,
            fuel_system="test",
            fuel_control="test",
            seat_height=100.0,
            cooling_system="test",
            color_options="test",
            url="test",
        )

        self.assertEqual(motorcycle.niv, "12345678901234567")
        self.assertEqual(motorcycle.brand, "test")
        self.assertEqual(motorcycle.model, "test")
        self.assertEqual(motorcycle.year, 2021)
        self.assertEqual(motorcycle.category, "test")
        self.assertEqual(motorcycle.rating, 5.0)
        self.assertEqual(motorcycle.displacement, 1000)
        self.assertEqual(motorcycle.power, 100.0)
        self.assertEqual(motorcycle.torque, 100)
        self.assertEqual(motorcycle.engine_cylinders, "test")
        self.assertEqual(motorcycle.engine_stroke, "test")
        self.assertEqual(motorcycle.gearbox, "test")
        self.assertEqual(motorcycle.bore, 100)
        self.assertEqual(motorcycle.stroke, 100.0)
        self.assertEqual(motorcycle.transmission_type, "test")
        self.assertEqual(motorcycle.front_brakes, "test")
        self.assertEqual(motorcycle.rear_brakes, "test")
        self.assertEqual(motorcycle.front_suspension, "test")
        self.assertEqual(motorcycle.rear_suspension, "test")
        self.assertEqual(motorcycle.front_tire, "test")
        self.assertEqual(motorcycle.rear_tire, "test")
        self.assertEqual(motorcycle.dry_weight, 1000)
        self.assertEqual(motorcycle.wheelbase, 1000)
        self.assertEqual(motorcycle.fuel_capacity, 1000)
        self.assertEqual(motorcycle.fuel_system, "test")
        self.assertEqual(motorcycle.fuel_control, "test")
        self.assertEqual(motorcycle.seat_height, 100.0)
        self.assertEqual(motorcycle.cooling_system, "test")
        self.assertEqual(motorcycle.color_options, "test")
        self.assertEqual(motorcycle.url, "test")
        self.assertEqual(
            motorcycle.__repr__(),
            f"Motorcycle>>> {motorcycle.brand} {motorcycle.model} {motorcycle.year}",
        )

    def test_not_found_error(self):
        response = self.client.get("/notfound")
        self.assertEqual(response.status_code, 404)

    def test_short_url(self):
        response = self.client.post(
            "/api/v1/auth/register",
            json={
                "username": "test",
                "email": "testuser@test.com",
                "password": "TestPassword123!",
            },
        )

        response = self.client.post(
            "/api/v1/auth/login",
            json={
                "email": "testuser@test.com",
                "password": "TestPassword123!",
            },
        )

        token = response.json["user"]["access"]

        response = self.client.post(
            "/api/v1/motorcycles/",
            json={
                "niv": "1HD1BWV1X7Y015039",
                "brand": "Honda",
                "model": "Cb500f",
                "year": 2022,
                "category": "Naked",
                "rating": 3.3,
                "displacement": 471,
                "power": 46.9,
                "torque": 43,
                "engine_cylinders": "Twin",
                "engine_stroke": "4-stroke",
                "gearbox": "6-speed",
                "bore": 67,
                "stroke": 66.8,
                "transmission_type": "Chain",
                "front_brakes": "Single disc",
                "rear_brakes": "Single disc",
                "front_suspension": "Showa 41mm SFF-BP USD forks, pre-load adjustable",
                "rear_suspension": "Prolink mono with 5 stage pre-load adjuster, steel hollow cross swingarm",
                "front_tire": "120/70-ZR17",
                "rear_tire": "190/50-ZR17",
                "dry_weight": 192,
                "wheelbase": 1410,
                "fuel_capacity": 790,
                "fuel_system": "Injection. PGM-FI with 34mm throttle bodies",
                "fuel_control": "Double Overhead Cams/Twin Cam (DOHC)",
                "seat_height": 16.7,
                "cooling_system": "Liquid",
                "color_options": "Grand Prix Red, Matt Axis Grey Metallic, Pearl Smokey Gray, Pearl Dusk Yellow",
                "url": "https://www.motorcyclespecs.co.za/model/Honda/honda_cb500f_22.html",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        niv = response.json["niv"]

        response = self.client.get(
            "/api/v1/motorcycles/" + niv,
            headers={"Authorization": f"Bearer {token}"},
        )

        short_url = response.json["data"]["short_url"]

        response = self.client.get(
            "/" + short_url,
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 302)
