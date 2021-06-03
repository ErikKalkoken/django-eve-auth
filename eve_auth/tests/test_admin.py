from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase

from ..admin import UserAdmin
from .utils import create_fake_user


class TestNotificationAdmin(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.modeladmin = UserAdmin(model=get_user_model(), admin_site=AdminSite())

    def test_should_return_charater_name_when_eve_character_exists(self):
        # given
        user = create_fake_user(1001, "Bruce Wayne")
        # when
        result = self.modeladmin._character_name(user)
        # then
        self.assertEqual(result, "Bruce Wayne")

    def test_should_return_none_when_user_has_no_eve_character(self):
        # given
        user = get_user_model().objects.create(username="dummy")
        # when
        result = self.modeladmin._character_name(user)
        # then
        self.assertIsNone(result)
