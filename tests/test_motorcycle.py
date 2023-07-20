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

    def createUser_getToken(self):
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

        return response.json["user"]["access"]

    def createMotorcycle(self):
        token = self.createUser_getToken()

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

        return response

    def test_motorcycle_invalidURL(self):
        token = self.createUser_getToken()

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
                "url": "chinaMotorcycles",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 400)

    def test_motorcycle_URL_alreadyExist(self):
        token = self.createUser_getToken()

        self.createMotorcycle()

        response = self.client.post(
            "/api/v1/motorcycles/",
            json={
                "niv": "1HD1BWV1X7Y021039",
                "brand": "Honda",
                "model": "Cb500f",
                "year": 2021,
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

        self.assertEqual(response.status_code, 409)

    def test_motorcycle_sameNIV(self):
        token = self.createUser_getToken()

        self.createMotorcycle()

        response = self.client.post(
            "/api/v1/motorcycles/",
            json={
                "niv": "1HD1BWV1X7Y015039",
                "brand": "Honda",
                "model": "Cb500f",
                "year": 2021,
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
                "url": "https://www.motorcyclespecs.co.za/model/Honda/honda_cb500f_21.html",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 409)

    def test_motorcycle_missing_parameter(self):
        token = self.createUser_getToken()

        response = self.client.post(
            "/api/v1/motorcycles/",
            json={
                "niv": "1HD1BWV1X7Y015039",
                "brand": "Honda",
                "model": "Cb500f",
                "year": 2021,
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
                "color_options": "Grand Prix Red, Matt Axis Grey Metallic, Pearl Smokey Gray, Pearl Dusk Yellow",
                "url": "https://www.motorcyclespecs.co.za/model/Honda/honda_cb500f_21.html",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 400)

    def test_motorcycle_getAllMotos(self):
        token = self.createUser_getToken()

        self.createMotorcycle()

        response = self.client.get(
            "/api/v1/motorcycles/",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 200)

    def test_motorcycle_getMoto_withParameters(self):
        token = self.createUser_getToken()

        self.createMotorcycle()

        response = self.client.get(
            "/api/v1/motorcycles/",
            headers={"Authorization": f"Bearer {token}"},
            query_string={
                "brand": "Honda",
                "model": "Cb500f",
                "year": 2022,
                "category": "Naked",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_motorcycle_getMoto_withWrongParameters(self):
        token = self.createUser_getToken()

        self.createMotorcycle()

        response = self.client.get(
            "/api/v1/motorcycles/",
            headers={"Authorization": f"Bearer {token}"},
            query_string={"wrong": "wrong"},
        )

        self.assertEqual(response.status_code, 400)

    def test_motorcycle_getNoMoto(self):
        token = self.createUser_getToken()

        response = self.client.get(
            "/api/v1/motorcycles/",
            headers={"Authorization": f"Bearer {token}"},
            query_string={
                "brand": "Yamaha",
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_motorcycle_dontFindSpecificMotorcycle(self):
        token = self.createUser_getToken()

        self.createMotorcycle()

        response = self.client.get(
            "/api/v1/motorcycles/1",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 404)

    def test_motorcycle_updateExistingMoto(self):
        token = self.createUser_getToken()

        self.createMotorcycle()

        response = self.client.put(
            "/api/v1/motorcycles/1HD1BWV1X7Y015039",
            json={
                "niv": "1HD1BWV1X7Y015039",
                "brand": "Honda",
                "model": "Cb500f",
                "year": 2021,
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
                "url": "https://www.motorcyclespecs.co.za/model/Honda/honda_cb500f_21.html",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 200)

    def test_motorcycle_updateExistingMoto_withWrongParameters(self):
        token = self.createUser_getToken()

        self.createMotorcycle()

        response = self.client.put(
            "/api/v1/motorcycles/1HD1BWV1X7Y015039",
            json={
                "niv": "1HD1BWV1X7Y015039",
                "brand": "Honda",
                "model": "Cb500f",
                "year": 2021,
                "category": "Naked",
                "rating": 3.3,
                "displacement": 471,
                "power": 46.9,
                "torque": 43,
                "engine_cylinders": "Twin",
                "engine_stroke": "4-stroke",
                "gearbox": "6-speed",
                "boreee": 67,
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
                "color_options": "Grand Prix Red, Matt Axis Grey Metallic, Pearl Smokey Gray, Pearl Dusk Yellow",
                "url": "https://www.motorcyclespecs.co.za/model/Honda/honda_cb500f_21.html",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 400)

    def test_motorcycle_updateExistingMoto_withWrongURL(self):
        token = self.createUser_getToken()

        self.createMotorcycle()

        response = self.client.put(
            "/api/v1/motorcycles/1HD1BWV1X7Y015039",
            json={
                "niv": "1HD1BWV1X7Y015039",
                "brand": "Honda",
                "model": "Cb500f",
                "year": 2021,
                "category": "Naked",
                "rating": 3.3,
                "displacement": 471,
                "power": 46.9,
                "torque": 43,
                "engine_cylinders": "Twin",
                "engine_stroke": "4-stroke",
                "gearbox": "6-speed",
                "boreee": 67,
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
                "color_options": "Grand Prix Red, Matt Axis Grey Metallic, Pearl Smokey Gray, Pearl Dusk Yellow",
                "url": "chinaMotorcycles",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 400)

    def test_motorcycle_updateExistingMoto_withURLalreadyExists(self):
        token = self.createUser_getToken()

        self.createMotorcycle()

        response = self.client.put(
            "/api/v1/motorcycles/1HD1BWV1X7Y015039",
            json={
                "niv": "1HD1BWV1X7Y015039",
                "brand": "Honda",
                "model": "Cb500f",
                "year": 2021,
                "category": "Naked",
                "rating": 3.3,
                "displacement": 471,
                "power": 46.9,
                "torque": 43,
                "engine_cylinders": "Twin",
                "engine_stroke": "4-stroke",
                "gearbox": "6-speed",
                "boreee": 67,
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
                "color_options": "Grand Prix Red, Matt Axis Grey Metallic, Pearl Smokey Gray, Pearl Dusk Yellow",
                "url": "https://www.motorcyclespecs.co.za/model/Honda/honda_cb500f_22.html",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 409)

    def test_motorcycle_updateExistingMoto_withWrongNIV(self):
        token = self.createUser_getToken()

        self.createMotorcycle()

        response = self.client.put(
            "/api/v1/motorcycles/2",
            json={
                "niv": "1HD1BWV1X7Y015040",
                "brand": "Honda",
                "model": "Cb500f",
                "year": 2021,
                "category": "Naked",
                "rating": 3.3,
                "displacement": 471,
                "power": 46.9,
                "torque": 43,
                "engine_cylinders": "Twin",
                "engine_stroke": "4-stroke",
                "gearbox": "6-speed",
                "boreee": 67,
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
                "color_options": "Grand Prix Red, Matt Axis Grey Metallic, Pearl Smokey Gray, Pearl Dusk Yellow",
                "url": "https://www.motorcyclespecs.co.za/model/Honda/honda_cb500f_21.html",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 404)

    def test_motorcycle_delete(self):
        token = self.createUser_getToken()

        self.createMotorcycle()

        response = self.client.delete(
            "/api/v1/motorcycles/1HD1BWV1X7Y015039",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 204)

    def test_motorcycle_delete_nonExistingMoto(self):
        token = self.createUser_getToken()

        self.createMotorcycle()

        response = self.client.delete(
            "/api/v1/motorcycles/2",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 404)

    def test_motorcycle_stats(self):
        token = self.createUser_getToken()

        self.createMotorcycle()

        response = self.client.get(
            "/api/v1/motorcycles/stats",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 200)
