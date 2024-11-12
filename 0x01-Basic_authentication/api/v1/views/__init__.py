#!/usr/bin/env python3
"""
Blueprint setup for the API views.

This module initializes the `app_views` Blueprint, which serves as the entry point
for various API routes under the `/api/v1` prefix. It also imports route handlers
and initializes any required data on startup.
"""
from flask import Blueprint

# Define the Blueprint for API routes with a URL prefix of `/api/v1`
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Importing routes for handling different endpoints
from api.v1.views.index import *
from api.v1.views.users import *

# Load user data from file upon initialization
User.load_from_file()
