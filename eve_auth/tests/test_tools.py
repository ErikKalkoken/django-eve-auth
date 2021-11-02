from django.test import TestCase

from eve_auth.tools.test_tools import add_permission_to_user_by_name, create_fake_user


class TestCreateFakeUser(TestCase):
    def test_should_create_simple_user(self):
        # when
        user = create_fake_user(1001, "Bruce Wayne")
        # then
        self.assertEqual(user.eve_character.character_id, 1001)
        self.assertEqual(user.eve_character.character_name, "Bruce Wayne")

    def test_should_create_user_with_permission(self):
        # when
        user = create_fake_user(
            1001, "Bruce Wayne", permissions=["eve_auth.add_userevecharacter"]
        )
        # then
        self.assertTrue(user.has_perm("eve_auth.add_userevecharacter"))

    def test_should_create_user_with_multiple_permission(self):
        # when
        user = create_fake_user(
            1001,
            "Bruce Wayne",
            permissions=[
                "eve_auth.add_userevecharacter",
                "eve_auth.change_userevecharacter",
            ],
        )
        # then
        self.assertTrue(user.has_perm("eve_auth.add_userevecharacter"))
        self.assertTrue(user.has_perm("eve_auth.change_userevecharacter"))

    def test_should_add_permission_to_existing_user(self):
        # given
        user = create_fake_user(1001, "Bruce Wayne")
        # when
        user = add_permission_to_user_by_name("eve_auth.add_userevecharacter", user)
        # then
        self.assertTrue(user.has_perm("eve_auth.add_userevecharacter"))

    def test_should_raise_error_when_permission_is_not_valid(self):
        # given
        user = create_fake_user(1001, "Bruce Wayne")
        # when/then
        with self.assertRaises(ValueError):
            add_permission_to_user_by_name("dummy", user)
