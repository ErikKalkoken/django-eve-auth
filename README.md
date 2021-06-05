# Eve Auth

Eve Auth enabled users to authenticate and login to a Django website using their Eve Online account

[![release](https://img.shields.io/pypi/v/django-eve-auth?label=release)](https://pypi.org/project/django-eve-auth/)
[![python](https://img.shields.io/pypi/pyversions/django-eve-auth)](https://pypi.org/project/django-eve-auth/)
[![django](https://img.shields.io/pypi/djversions/django-eve-auth?label=django)](https://pypi.org/project/django-eve-auth/)
[![pipeline](https://gitlab.com/ErikKalkoken/django-eve-auth/badges/master/pipeline.svg)](https://gitlab.com/ErikKalkoken/django-eve-auth/-/pipelines)
[![codecov](https://codecov.io/gl/ErikKalkoken/django-eve-auth/branch/master/graph/badge.svg?token=DXGHIE3BJ1)](https://codecov.io/gl/ErikKalkoken/django-eve-auth)
[![license](https://img.shields.io/badge/license-MIT-green)](https://gitlab.com/ErikKalkoken/django-eve-auth/-/blob/master/LICENSE)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Settings](#settings)
- [Change Log](CHANGELOG.md)

## Features

- Users can login via EVE SSO. New user accounts will automatically be created from the Eve character.
- Users keep their accounts as long as the character does not change ownership
- User's character name is updated with every new login
- Supports Django's default login URLs and next parameter
- Also includes a template tag for creating user icons with the related eve character portrait
- Fully tested

## Technical overview

Eve Auth is designed to be used with [django-esi](https://gitlab.com/allianceauth/django-esi) for accessing ESI. Conceptually it is an extension of django-esi.

Newly created users are stored with the Eve character the user logged in with. This allows users to be treated as eve characters and vice versa. You can access the eve character like so:

>**Note**<br>The relation between user and character is one-to-one only. Multiple character ownerships are not supported.

Users are identified through the SSO owner hash of their character. This hash will change when the ownership of a character changes. If that happens a new user account will be created for that character.

After login, a SSO token is stored for each user, which can be later used for accessing ESI through the django-esi API. By default logins do not require any ESI scopes, but you can add scopes via the setting `EVE_AUTH_LOGIN_SCOPES` (See [Settings](#settings) for details).

## Installation

### Step 1 - Dependencies

Please install and add [django-esi](https://gitlab.com/allianceauth/django-esi) to your Django site.

### Step 2 - Install app

Make sure you are in the virtual environment (venv) of your Alliance Auth installation. Then install the newest release from PyPI:

```bash
pip install django-eve-auth
```

### Step 2 - Configure Auth settings

Configure your Django settings as follows:

- Add `"eve_auth"` to your `INSTALLED_APPS`
- Add `"eve_auth.backends.EveSSOBackend"` to `AUTHENTICATION_BACKENDS`. Make sure it is the first in the list.
- Set `LOGIN_URL`, `LOGOUT_REDIRECT_URL` and `LOGIN_REDIRECT_URL` to the corresponding view names of your site.
- Optional: Add additional settings if you want to change any defaults. See [Settings](#settings) for the full list.

### Step 3 - Include URLs

Make sure that the Eve Auth URLs are enabled for your site. e.g. with the following entry in your global urls.py:

```python
urlpatterns = [
    ...
    path("eve_auth/", include("eve_auth.urls")),
    ...
]
```

### Step 4 - Finalize App installation

Run migrations & copy static files

```bash
python manage.py migrate
python manage.py collectstatic
```

Restart your Django server.

## Usage

### User login/logout

Eve Auth comes with predefined views for logging and logging out users. To use them simple redirect to the respective view, e.g. in your template:

- login: `eve_auth:login`
- logout: `eve_auth:logout`

Here is a simple example for creating a login link in a Django template:

```jinja
<a href="{% url 'eve_auth:login' %}">Login</a>
```

Both login and logout support the `next` parameter. Here is an example snippet for returning to the current page after successful login:

```jinja
<a href="{% url 'eve_auth:login' %}?next=request.path">Login</a>
```

### Accessing the eve character of a user

A user is always linked to their eve character. You can access the eve character from a user objects via the `eve_character` property. Here is a simple example for printing the related character ID for a user:

```python
user = User.objects.get(pk)
print(user.eve_character.character_id)
```

### User icon template tags

To use the template tag you need to first load it on your template:

```jinja
{% load eve_auth %}
```

Then you can use them like shown below, where `user` is an user object that has been created by this app and thus has an `eve_character` property:

```jinja
{% user_icon user %}
```

This will create a user icon with the default size as defined by `EVE_AUTH_USER_ICON_DEFAULT_SIZE`. You can also define a custom size like so:

```jinja
{% user_icon user 128 %}
```

You can also customize the user icons by adding styles for the CSS class `eve-auth-user-icon`.

### Custom user profile

If you need to add custom information to an user object for your site  - e.g. a user profile - you can use the standard approach for extending the User model with an one-two-one relation. This is explained in detail in this chapter of the official Django documentation: [Extending the existing User model](https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#extending-the-existing-user-model)

### Tests

If you need to create users with eve characters for your unit tests please check out our the test tools at `eve_auth.tools.test_tools`:

## Settings

Here is a list of available settings for this app. They can be configured by adding them to your AA settings file (`local.py`).

Note that all settings are optional and the app will use the documented default settings if they are not defined.

Name | Description | Default
-- | -- | --
`EVE_AUTH_LOGIN_SCOPES`| List of ESI scope names to be requested with every login. e.g. `['esi-universe.read_structures.v1', 'esi-search.search_structures.v1']`. The default will not request any scopes.  | `[]`
`EVE_AUTH_USER_ICON_DEFAULT_SIZE`| Default size of user icons in pixel. | `24`
