from django.test import TestCase

from .utils import create_fake_user


class TestUserEveCharacter(TestCase):
    def test_should_return_character_name(self):
        # given
        user = create_fake_user(1001, "Bruce Wayne")
        # when
        result = str(user.eve_character)
        # then
        self.assertEqual(result, "Bruce Wayne")

    def test_should_return_portrait_url(self):
        # given
        user = create_fake_user(1001, "Bruce Wayne")
        # when
        result = user.eve_character.character_portrait_url()
        # then
        self.assertEqual(
            result, "https://images.evetech.net/characters/1001/portrait?size=32"
        )

    def test_should_return_portrait_url_with_custom_size(self):
        # given
        user = create_fake_user(1001, "Bruce Wayne")
        # when
        result = user.eve_character.character_portrait_url(128)
        # then
        self.assertEqual(
            result, "https://images.evetech.net/characters/1001/portrait?size=128"
        )

    def test_should_raise_error_when_size_not_int(self):
        # given
        user = create_fake_user(1001, "Bruce Wayne")
        # when
        with self.assertRaises(ValueError):
            user.eve_character.character_portrait_url("invalid")

    def test_should_raise_error_when_size_not_valid_1(self):
        # given
        user = create_fake_user(1001, "Bruce Wayne")
        # when
        with self.assertRaises(ValueError):
            user.eve_character.character_portrait_url(16)

    def test_should_raise_error_when_size_not_valid_2(self):
        # given
        user = create_fake_user(1001, "Bruce Wayne")
        # when
        with self.assertRaises(ValueError):
            user.eve_character.character_portrait_url(2048)

    def test_should_raise_value_error_when_size_not_valid_3(self):
        # given
        user = create_fake_user(1001, "Bruce Wayne")
        # when
        with self.assertRaises(ValueError):
            user.eve_character.character_portrait_url(31)
