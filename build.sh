#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies from requirements.txt
pip install -r requirements.txt

python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput