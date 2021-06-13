# Developer Guide

The developer guide describes how to develop apps with *django-eve-auth*.

## Overview

Eve Auth is designed to be used with [django-esi](https://gitlab.com/allianceauth/django-esi) for accessing ESI. Conceptually it is an extension of django-esi.

Newly created users are stored with the Eve character the user logged in with. This allows users to be treated as eve characters and vice versa. You can access the eve character like so:

```eval_rst
.. note::
    The relation between user and character is one-to-one only. Multiple character ownerships are not supported.
```

Users are identified through the SSO owner hash of their character. This hash will change when the ownership of a character changes. If that happens a new user account will be created for that character.

After login, a SSO token is stored for each user, which can be later used for accessing ESI through the django-esi API. By default logins do not require any ESI scopes, but you can add scopes via the setting `EVE_AUTH_LOGIN_SCOPES` (See [Settings](#settings) for details).

## User login/logout

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

## Accessing the eve character of a user

A user is always linked to their eve character. You can access the eve character from a user objects via the `eve_character` property. Here is a simple example for printing the related character ID for a user:

```python
user = User.objects.get(pk)
print(user.eve_character.character_id)
```

## User icon template tags

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

## Custom user profile

If you need to add custom information to an user object for your site  - e.g. a user profile - you can use the standard approach for extending the User model with an one-two-one relation. This is explained in detail in this chapter of the official Django documentation: [Extending the existing User model](https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#extending-the-existing-user-model)

## Tests

If you need to create users with eve characters for your unit tests Eve Auth is providing a tools for creating fake users and fake tokens.

```eval_rst
.. seealso::
    Please see :ref:`api-tools` for the test tools.
```
