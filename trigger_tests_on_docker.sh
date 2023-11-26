#!/bin/bash
set -xe

pip install .[testing]
pytest --cov=credcrud --cov-report xml:coverage.xml --cov-report term
