#!/bin/bash
set -xe

pip install .[testing]
pytest --cov --cov-report xml:coverage.xml --cov-report term
