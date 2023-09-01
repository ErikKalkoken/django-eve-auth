from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse
from esi.models import Token

from eve_auth.tools.test_tools import create_fake_token, create_fake_user

from .. import views

MODULE_BACKEND = "eve_auth.backends"
MODULE_VIEWS = "eve_auth.views"

OWNER_HASH = "owner-hash"
OAUTH_TOKEN_URL = "https://login.eveonline.com/v2/oauth/token"


def fake_token(owner_hash, user=None):
    return create_fake_token(
        character_id=1001,
        character_name="Bruce Wayne",
        character_owner_hash=owner_hash,
        user=user,
    )


@patch(MODULE_VIEWS + ".app_settings.EVE_AUTH_LOGIN_SCOPES", "publicData")
@patch(MODULE_VIEWS + ".settings.LOGIN_URL", "/login-failed")
@patch(MODULE_VIEWS + ".settings.LOGIN_REDIRECT_URL", "/login-success")
class TestLogin(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.factory = RequestFactory()

    def login(self, token, next_url=None):
        url = reverse("eve_auth:login")
        if next_url:
            url += f"?next={next_url}"
        request = self.factory.get(url)
        middleware = SessionMiddleware(Mock())
        middleware.process_request(request)
        request.session.save()
        orig_view = views.login.__wrapped__
        return request, orig_view(request, token)

    def test_should_create_and_login_new_user(self):
        # given
        new_login_token = fake_token(OWNER_HASH)
        # when
        request, response = self.login(new_login_token)
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login-success")
        self.assertIn("_auth_user_id", request.session)
        user = User.objects.get(pk=request.session["_auth_user_id"])
        self.assertEqual(user.first_name, "Bruce")
        self.assertEqual(user.last_name, "Wayne")
        self.assertEqual(user.eve_character.character_id, 1001)
        self.assertEqual(user.eve_character.character_name, "Bruce Wayne")
        self.assertEqual(user.eve_character.character_owner_hash, OWNER_HASH)

    def test_should_login_existing_user(self):
        # given
        new_login_token = fake_token(OWNER_HASH)
        existing_user = create_fake_user(1001, "Bruce Wayne", OWNER_HASH)
        # when
        request, response = self.login(new_login_token)
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login-success")
        self.assertIn("_auth_user_id", request.session)
        user = User.objects.get(pk=request.session["_auth_user_id"])
        self.assertEqual(existing_user, user)

    def test_should_update_character_name_when_logging_in_existing_user(self):
        # given
        new_login_token = fake_token(OWNER_HASH)
        existing_user = create_fake_user(1001, "Bruce Wayne", OWNER_HASH)
        existing_user.fist_name = "Peter"
        existing_user.last_name = "Parker"
        existing_user.save()
        existing_user.eve_character.character_name = "Peter Parker"
        existing_user.eve_character.save()
        # when
        request, response = self.login(new_login_token)
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login-success")
        self.assertIn("_auth_user_id", request.session)
        user = User.objects.get(pk=request.session["_auth_user_id"])
        self.assertEqual(existing_user, user)
        self.assertEqual(user.eve_character.character_name, "Bruce Wayne")

    def test_should_create_and_login_new_user_when_owner_has_changed(self):
        # given
        new_login_token = fake_token("new-owner-hash")
        existing_user = create_fake_user(1001, "Bruce Wayne", OWNER_HASH)
        # when
        request, response = self.login(new_login_token)
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login-success")
        self.assertIn("_auth_user_id", request.session)
        user = User.objects.get(pk=request.session["_auth_user_id"])
        self.assertNotEqual(existing_user, user)
        self.assertEqual(user.first_name, "Bruce")
        self.assertEqual(user.last_name, "Wayne")
        self.assertEqual(user.eve_character.character_id, 1001)
        self.assertEqual(user.eve_character.character_name, "Bruce Wayne")
        self.assertEqual(user.eve_character.character_owner_hash, "new-owner-hash")

    @patch(MODULE_VIEWS + ".messages")
    def test_should_not_login_when_user_is_deactivated(self, messages):
        # given
        new_login_token = fake_token(OWNER_HASH)
        existing_user = create_fake_user(1001, "Bruce Wayne", OWNER_HASH)
        existing_user.is_active = False
        existing_user.save()
        # when
        request, response = self.login(new_login_token)
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
        new_login_token = fake_token(OWNER_HASH)
        create_fake_user(1001, "Bruce Wayne", OWNER_HASH)
        # when
        request, response = self.login(new_login_token)
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login-failed")
        self.assertNotIn("_auth_user_id", request.session)
        self.assertTrue(messages.error.called)

    def test_should_delete_new_login_token_if_user_already_exists(self):
        # given
        existing_user = create_fake_user(1001, "Bruce Wayne", OWNER_HASH)
        new_login_token = fake_token(OWNER_HASH)
        # when
        request, response = self.login(new_login_token)
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login-success")
        self.assertEqual(int(request.session["_auth_user_id"]), existing_user.id)
        self.assertFalse(Token.objects.filter(pk=new_login_token.pk).exists())

    def test_should_login_existing_user_and_redirect_to_next(self):
        # given
        new_login_token = fake_token(OWNER_HASH)
        existing_user = create_fake_user(1001, "Bruce Wayne", OWNER_HASH)
        # when
        request, response = self.login(new_login_token, next_url="/new-page")
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/new-page")
        self.assertIn("_auth_user_id", request.session)
        user = User.objects.get(pk=request.session["_auth_user_id"])
        self.assertEqual(existing_user, user)


@patch(MODULE_VIEWS + ".settings.LOGIN_URL", "/logged-out")
class TestLogout(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.factory = RequestFactory()
        cls.user = create_fake_user(1001, "Bruce Wayne", OWNER_HASH)

    @override_settings(LOGIN_URL="/logged-out")
    def test_should_logout_user_with_default_redirect(self):
        # given
        request = self.factory.get(reverse("eve_auth:login"))
        request.user = self.user
        middleware = SessionMiddleware(Mock())
        middleware.process_request(request)
        request.session.save()
        # when
        response = views.logout(request)
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/logged-out")
        self.assertFalse(request.user.is_authenticated)

    def test_should_logout_user_and_redirect_to_next(self):
        # given
        url = reverse("eve_auth:login") + "?next=/new-page"
        request = self.factory.get(url)
        request.user = self.user
        middleware = SessionMiddleware(Mock())
        middleware.process_request(request)
        request.session.save()
        # when
        response = views.logout(request)
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/new-page")
        self.assertFalse(request.user.is_authenticated)

    @override_settings(LOGOUT_REDIRECT_URL="/logged-out-2")
    def test_should_logout_user_and_redirect_to_logout_url(self):
        # given
        request = self.factory.get(reverse("eve_auth:login"))
        request.user = self.user
        middleware = SessionMiddleware(Mock())
        middleware.process_request(request)
        request.session.save()
        # when
        response = views.logout(request)
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/logged-out-2")
        self.assertFalse(request.user.is_authenticated)
