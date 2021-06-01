from django.test import RequestFactory, TestCase
from django.urls import reverse

from ..backends import EveSSOBackend
from .utils import create_fake_user


class TestEveSSOBackendAuthenticate(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.factory = RequestFactory()

    def test_should_return_none_when_no_token_provided(self):
        # given
        backend = EveSSOBackend()
        request = self.factory.get(reverse("eve_auth:login"))
        # when
        result = backend.authenticate(request, token=None)
        # then
        self.assertIsNone(result)

    def test_should_return_none_when_token_has_wrong_type(self):
        # given
        backend = EveSSOBackend()
        request = self.factory.get(reverse("eve_auth:login"))
        # when
        result = backend.authenticate(request, token="invalid")
        # then
        self.assertIsNone(result)


class TestEveSSOBackendGetUser(TestCase):
    def test_should_return_user(self):
        # given
        user = create_fake_user(1001, "Bruce Wayne")
        backend = EveSSOBackend()
        # when
        result = backend.get_user(user_id=user.id)
        # then
        self.assertEqual(result, user)

    def test_should_return_none(self):
        # given
        backend = EveSSOBackend()
        # when
        result = backend.get_user(user_id=1)
        # then
        self.assertIsNone(result)
