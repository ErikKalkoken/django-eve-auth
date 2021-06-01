from unittest.mock import patch

from django.test import TestCase

from ..app_settings import get_setting_or_default

MODULE_PATH = "eve_auth.app_settings"


class TestGetSettingOrDefault(TestCase):
    @patch(MODULE_PATH + ".settings")
    def test_should_return_value_if_set(self, settings):
        # given
        settings.EVE_AUTH_LOGIN_URL = "my-url"
        # when
        result = get_setting_or_default("EVE_AUTH_LOGIN_URL", "/")
        # then
        self.assertEqual(result, "my-url")

    @patch(MODULE_PATH + ".settings", object())
    def test_should_return_default_if_not_set(self):
        # when
        result = get_setting_or_default("EVE_AUTH_LOGIN_URL", "/")
        # then
        self.assertEqual(result, "/")

    @patch(MODULE_PATH + ".settings")
    def test_should_return_default_if_wrong_type(self, settings):
        # given
        settings.EVE_AUTH_LOGIN_URL = []
        # when
        result = get_setting_or_default("EVE_AUTH_LOGIN_URL", "/")
        # then
        self.assertEqual(result, "/")
