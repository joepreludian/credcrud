#!/bin/bash
set -xe

pip install .[testing]
pytest --cov
