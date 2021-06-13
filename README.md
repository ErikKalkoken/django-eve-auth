# Eve Auth

Eve Auth enables users to authenticate and login to a Django website using their Eve Online account.

[![release](https://img.shields.io/pypi/v/django-eve-auth?label=release)](https://pypi.org/project/django-eve-auth/)
[![python](https://img.shields.io/pypi/pyversions/django-eve-auth)](https://pypi.org/project/django-eve-auth/)
[![django](https://img.shields.io/pypi/djversions/django-eve-auth?label=django)](https://pypi.org/project/django-eve-auth/)
[![pipeline](https://gitlab.com/ErikKalkoken/django-eve-auth/badges/master/pipeline.svg)](https://gitlab.com/ErikKalkoken/django-eve-auth/-/pipelines)
[![codecov](https://codecov.io/gl/ErikKalkoken/django-eve-auth/branch/master/graph/badge.svg?token=DXGHIE3BJ1)](https://codecov.io/gl/ErikKalkoken/django-eve-auth)
[![Documentation Status](https://readthedocs.org/projects/django-eve-auth/badge/?version=latest)](https://django-eve-auth.readthedocs.io/en/latest/?badge=latest)
[![license](https://img.shields.io/badge/license-MIT-green)](https://gitlab.com/ErikKalkoken/django-eve-auth/-/blob/master/LICENSE)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![chat](https://img.shields.io/discord/790364535294132234)](https://discord.gg/zmh52wnfvM)

## Features

- Users can login via EVE SSO. New user accounts will automatically be created from the Eve character.
- Users keep their accounts as long as the character does not change ownership
- User's character name is updated with every new login
- Supports Django's default login URLs and next parameter
- Also includes a template tag for creating user icons with the related eve character portrait
- Fully tested

## Documentation

For all details on how to install and use Eve Auth please see the [documentation](https://django-eve-auth.readthedocs.io/en/latest/).
