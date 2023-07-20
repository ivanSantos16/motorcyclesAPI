import unittest
from src.config.config import config_dict
from src import create_app
from src.database import db, User


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

    def test_user_register(self):
        response = self.client.post(
            "/api/v1/auth/register",
            json={
                "username": "test",
                "email": "testuser@test.com",
                "password": "TestPassword123!",
            },
        )

        user = User.query.filter_by(email="testuser@test.com").first()

        self.assertEqual(user.username, "test")
        self.assertEqual(user.email, "testuser@test.com")
        self.assertEqual(response.status_code, 201)

    def test_user_register_invalid_email(self):
        response = self.client.post(
            "/api/v1/auth/register",
            json={
                "username": "test",
                "email": "testuser",
                "password": "TestPassword123!",
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_user_register_invalid_password(self):
        response = self.client.post(
            "/api/v1/auth/register",
            json={
                "username": "test",
                "email": "testuser@test.com",
                "password": "testpassword",
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_user_register_invalid_username(self):
        response = self.client.post(
            "/api/v1/auth/register",
            json={
                "username": "te",
                "email": "testuser@test.com",
                "password": "testpassword",
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_user_register_email_already_used(self):
        self.client.post(
            "/api/v1/auth/register",
            json={
                "username": "test",
                "email": "testuser@test.com",
                "password": "testpassword",
            },
        )

        response = self.client.post(
            "/api/v1/auth/register",
            json={
                "username": "test2",
                "email": "testuser@test.com",
                "password": "testpassword",
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_user_login(self):
        self.client.post(
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

        self.assertEqual(response.status_code, 200)

    def test_user_login_badCredentials(self):
        self.client.post(
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
                "password": "TestPassword",
            },
        )

        self.assertEqual(response.status_code, 401)

    def test_user_me(self):
        self.client.post(
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
                "email": "test",
                "email": "testuser@test.com",
                "password": "TestPassword123!",
            },
        )

        token = response.json["user"]["access"]

        response = self.client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 200)

    def test_user_me_invalid_token(self):
        token = "test"
        response = self.client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 422)

    def test_user_me_no_token(self):
        response = self.client.get(
            "/api/v1/auth/me",
        )

        self.assertEqual(response.status_code, 401)

    def test_user_refresh_token(self):
        self.client.post(
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
                "username": "test",
                "email": "testuser@test.com",
                "password": "TestPassword123!",
            },
        )

        refresh_token = response.json["user"]["refresh"]

        response = self.client.get(
            "/api/v1/auth/token/refresh",
            headers={"Authorization": f"Bearer {refresh_token}"},
        )

        self.assertEqual(response.status_code, 200)

    def test_user_refresh_token_invalid_token(self):
        refresh_token = "test"
        response = self.client.get(
            "/api/v1/auth/token/refresh",
            headers={"Authorization": f"Bearer {refresh_token}"},
        )

        self.assertEqual(response.status_code, 422)

    def test_user_password_less_than_8_characters(self):
        response = self.client.post(
            "/api/v1/auth/register",
            json={
                "username": "test",
                "email": "test@email.com",
                "password": "Test123",
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_user_password_no_uppercase(self):
        response = self.client.post(
            "/api/v1/auth/register",
            json={
                "username": "test",
                "email": "test@email.com",
                "password": "test123!",
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_user_password_no_lowercase(self):
        response = self.client.post(
            "/api/v1/auth/register",
            json={
                "username": "test",
                "email": "test@email.com",
                "password": "TEST123!",
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_user_password_no_special(self):
        response = self.client.post(
            "/api/v1/auth/register",
            json={
                "username": "test",
                "email": "test@email.com",
                "password": "Test1234",
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_user_less_than_3_characters(self):
        response = self.client.post(
            "/api/v1/auth/register",
            json={
                "username": "te",
                "email": "test@email.com",
                "password": "Test1234!",
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_user_email_already_exists(self):
        self.client.post(
            "/api/v1/auth/register",
            json={
                "username": "test",
                "email": "test@email.com",
                "password": "Test123!",
            },
        )

        response = self.client.post(
            "/api/v1/auth/register",
            json={
                "username": "test2",
                "email": "test@email.com",
                "password": "Test123!",
            },
        )

        self.assertEqual(response.status_code, 409)

    def test_user_same_username(self):
        self.client.post(
            "/api/v1/auth/register",
            json={
                "username": "test",
                "email": "test@email.com",
                "password": "Test123!",
            },
        )

        response = self.client.post(
            "/api/v1/auth/register",
            json={
                "username": "test",
                "email": "test2@email.com",
                "password": "Test123!",
            },
        )

        self.assertEqual(response.status_code, 409)

    def test_user_login_invalid_email(self):
        self.client.post(
            "/api/v1/auth/register",
            json={
                "username": "test",
                "email": "test@email.com",
                "password": "TEST123!",
            },
        )

        response = self.client.post(
            "/api/v1/auth/login",
            json={
                "email": "test",
                "password": "TEST123!",
            },
        )

        self.assertEqual(response.status_code, 401)

    def test_user_with_space(self):
        response = self.client.post(
            "/api/v1/auth/register",
            json={
                "username": "testtest ",
                "email": "test@email.com",
                "password": "Test123!",
            },
        )

        self.assertEqual(response.status_code, 400)
