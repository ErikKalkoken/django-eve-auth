from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase
from django.urls import reverse
from esi.models import Token

from .. import views
from .utils import create_fake_user

MODULE_BACKEND = "eve_auth.backends"
MODULE_VIEWS = "eve_auth.views"

OWNER_HASH = "owner-hash"
OAUTH_TOKEN_URL = "https://login.eveonline.com/v2/oauth/token"


def create_fake_token(owner_hash, user=None):
    return Token.objects.create(
        access_token="access-token",
        character_id=1001,
        character_name="Bruce Wayne",
        token_type="Character",
        character_owner_hash=owner_hash,
        user=user,
    )


@patch(MODULE_VIEWS + ".app_settings.LOGIN_TOKEN_SCOPES", "publicData")
@patch(MODULE_VIEWS + ".app_settings.LOGIN_URL", "/login-failed")
@patch(MODULE_VIEWS + ".app_settings.LOGIN_SUCCESS_URL", "/login-success")
class TestLogin(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def login(self, token):
        request = self.factory.get(reverse("eve_auth:login"))
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        orig_view = views.login.__wrapped__
        return request, orig_view(request, token)

    def test_should_create_and_login_new_user(self):
        # given
        token = create_fake_token(OWNER_HASH)
        # when
        request, response = self.login(token)
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login-success")
        self.assertIn("_auth_user_id", request.session)
        user = User.objects.get(pk=request.session["_auth_user_id"])
        self.assertEqual(user.first_name, "Bruce")
        self.assertEqual(user.last_name, "Wayne")
        self.assertEqual(user.eve_profile.character_name, "Bruce Wayne")
        self.assertEqual(user.eve_profile.character_id, 1001)
        self.assertEqual(user.eve_profile.owner_hash, OWNER_HASH)

    def test_should_login_existing_user(self):
        # given
        token = create_fake_token(OWNER_HASH)
        my_user = create_fake_user(1001, "Bruce Wayne", OWNER_HASH)
        # when
        request, response = self.login(token)
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login-success")
        self.assertIn("_auth_user_id", request.session)
        user = User.objects.get(pk=request.session["_auth_user_id"])
        self.assertEqual(my_user, user)

    def test_should_create_and_login_new_user_when_owner_has_changed(self):
        # given
        token = create_fake_token("new-owner-hash")
        my_user = create_fake_user(1001, "Bruce Wayne", OWNER_HASH)
        # when
        request, response = self.login(token)
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login-success")
        self.assertIn("_auth_user_id", request.session)
        user = User.objects.get(pk=request.session["_auth_user_id"])
        self.assertNotEqual(my_user, user)
        self.assertEqual(user.first_name, "Bruce")
        self.assertEqual(user.last_name, "Wayne")
        self.assertEqual(user.eve_profile.character_name, "Bruce Wayne")
        self.assertEqual(user.eve_profile.character_id, 1001)
        self.assertEqual(user.eve_profile.owner_hash, "new-owner-hash")

    @patch(MODULE_VIEWS + ".messages")
    def test_should_not_login_when_user_is_deactivate(self, messages):
        # given
        token = create_fake_token(OWNER_HASH)
        my_user = create_fake_user(1001, "Bruce Wayne", OWNER_HASH)
        my_user.is_active = False
        my_user.save()
        # when
        request, response = self.login(token)
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login-failed")
        self.assertNotIn("_auth_user_id", request.session)
        self.assertTrue(messages.warning.called)

    @patch(MODULE_VIEWS + ".messages")
    @patch(MODULE_VIEWS + ".auth.authenticate")
    def test_should_not_login_when_authentication_failed(self, authenticate, messages):
        # given
        authenticate.return_value = None
        token = create_fake_token(OWNER_HASH)
        my_user = create_fake_user(1001, "Bruce Wayne", OWNER_HASH)
        my_user.is_active = False
        my_user.save()
        # when
        request, response = self.login(token)
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login-failed")
        self.assertNotIn("_auth_user_id", request.session)
        self.assertTrue(messages.error.called)

    def test_should_delete_redundant_tokens(self):
        # given
        token = create_fake_token(OWNER_HASH)
        user = create_fake_user(1001, "Bruce Wayne", OWNER_HASH)
        create_fake_token(OWNER_HASH, user)
        # when
        request, response = self.login(token)
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login-success")
        self.assertIn("_auth_user_id", request.session)
        self.assertTrue(
            User.objects.filter(pk=request.session["_auth_user_id"]).exists()
        )
        self.assertEqual(Token.objects.filter(user=user).count(), 1)


@patch(MODULE_VIEWS + ".app_settings.LOGIN_URL", "/logged-out")
class TestLogout(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_should_logout_user(self):
        # given
        user = create_fake_user(1001, "Bruce Wayne", OWNER_HASH)
        request = self.factory.get(reverse("eve_auth:login"))
        request.user = user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        # when
        response = views.logout(request)
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/logged-out")
        self.assertFalse(request.user.is_authenticated)
