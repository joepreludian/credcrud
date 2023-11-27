#!/bin/bash
set -xe

pip install .[testing]
RSA_KEY_PASSWORD=MYPASSWORD pytest --cov=credcrud --cov-report xml:coverage.xml --cov-report term
