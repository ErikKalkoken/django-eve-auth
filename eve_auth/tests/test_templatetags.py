from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.template import Context, Template
from django.test import TestCase

from .utils import create_fake_user

CHARACTER_IMAGE_URL_BASE = "https://images.evetech.net/characters"


class TestUserIcon(TestCase):
    @patch(
        "eve_auth.templatetags.eve_auth.app_settings.EVE_AUTH_USER_ICON_DEFAULT_SIZE",
        24,
    )
    def test_should_render_html_for_user_default_size(self):
        # given
        template = Template("{% load eve_auth %}{% user_icon user %}")
        user = create_fake_user(1001, "User Bruce Wayne")
        context = Context({"user": user})
        # when
        result = template.render(context)
        # then
        self.assertEqual(
            result,
            (
                '<img class="eve-auth-user-icon" '
                f'src="{CHARACTER_IMAGE_URL_BASE}/1001/portrait?size=32" '
                'alt="User Bruce Wayne" width="24" height="24">\n'
            ),
        )

    def test_should_return_portrait_url_for_user_with_sizes(self):
        for size in [32, 64, 128, 256, 512, 1024]:
            # given
            template = Template(
                "{% load eve_auth %}{% user_icon user " + str(size) + " %}"
            )
            user = create_fake_user(1001, "User Bruce Wayne")
            context = Context({"user": user})
            # when
            result = template.render(context)
            # then
            self.assertEqual(
                result,
                (
                    '<img class="eve-auth-user-icon" '
                    f'src="{CHARACTER_IMAGE_URL_BASE}/1001/portrait?size={size}" '
                    f'alt="User Bruce Wayne" width="{size}" height="{size}">\n'
                ),
            )

    def test_should_return_portrait_url_for_user_with_size_overshoot(self):
        # given
        template = Template("{% load eve_auth %}{% user_icon user 2000 %}")
        user = create_fake_user(1001, "User Bruce Wayne")
        context = Context({"user": user})
        # when
        result = template.render(context)
        # then
        self.assertEqual(
            result,
            (
                '<img class="eve-auth-user-icon" '
                f'src="{CHARACTER_IMAGE_URL_BASE}/1001/portrait?size=1024" '
                'alt="User Bruce Wayne" width="2000" height="2000">\n'
            ),
        )

    def test_should_return_portrait_url_for_user_with_size_undershoot(self):
        # given
        template = Template("{% load eve_auth %}{% user_icon user 16 %}")
        user = create_fake_user(1001, "User Bruce Wayne")
        context = Context({"user": user})
        # when
        result = template.render(context)
        # then
        self.assertEqual(
            result,
            (
                '<img class="eve-auth-user-icon" '
                f'src="{CHARACTER_IMAGE_URL_BASE}/1001/portrait?size=32" '
                'alt="User Bruce Wayne" width="16" height="16">\n'
            ),
        )

    def test_should_return_dummy_portrait_for_invalid_input(self):
        # given
        template = Template("{% load eve_auth %}{% user_icon 'invalid' %}")
        user = create_fake_user(1001, "User Bruce Wayne")
        context = Context({"user": user})
        # when
        result = template.render(context)
        # then
        self.assertEqual(
            result,
            (
                '<img class="eve-auth-user-icon" '
                f'src="{CHARACTER_IMAGE_URL_BASE}/1/portrait?size=32" '
                'alt="" width="24" height="24">\n'
            ),
        )

    def test_should_return_dummy_portrait_when_user_has_not_eve_character(self):
        # given
        template = Template("{% load eve_auth %}{% user_icon 'invalid' %}")
        user = get_user_model().objects.create(username="dummy")
        context = Context({"user": user})
        # when
        result = template.render(context)
        # then
        self.assertEqual(
            result,
            (
                '<img class="eve-auth-user-icon" '
                f'src="{CHARACTER_IMAGE_URL_BASE}/1/portrait?size=32" '
                'alt="" width="24" height="24">\n'
            ),
        )
