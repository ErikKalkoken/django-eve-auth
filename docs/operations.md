# Operations Guide

The operations guide describes how to install, configure and maintain *django-eve-auth*.

## Installation

To install django-eve-auth into your Django project please follow these steps:

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

## Settings

Here is a list of available settings for this app. They can be configured by adding them to your local Django settings file.

```eval_rst
    .. |br| raw:: html

        <br>

    .. list-table:: Settings

        *   - Name
            - Description
            - Default
        *   - `EVE_AUTH_LOGIN_SCOPES`
            - List of ESI scope names to be requested with every login. e.g. `['esi-universe.read_structures.v1', 'esi-search.search_structures.v1']`. The default will not request any scopes.
            - `[]`
        *   - `EVE_AUTH_USER_ICON_DEFAULT_SIZE`
            - Default size of user icons in pixel.
            - `24`
```
