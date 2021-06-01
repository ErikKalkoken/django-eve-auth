# Eve Auth

## Overview

Eve Auth enabled users to authenticate and login to a Django website using their Eve Online account

- Users can authenticate through Eve Online SSO
- New users are automatically created as needed and linked to the Eve Online SSO account
- When characters change ownership they can no longer login to the previous account for security reasons

## Installation

- This app requires django-esi to be installed

## Settings

In addition to the settings from django-esi the following settings needs to be made:

- `EVE_AUTH_LOGIN_SUCCESS_URL`: name of view of path to redirect to after successful login
- `EVE_AUTH_LOGIN_SCOPES`: scopes for login
- `EVE_AUTH_LOGIN_URL`: name of view or path to redirect to when login failed
- `EVE_AUTH_USER_ICON_DEFAULT_SIZE`: Default size of user icons
