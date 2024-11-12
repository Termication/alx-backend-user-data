#!/usr/bin/env python3
"""
Module containing API index views.
Handles various endpoints for status checks and error testing.
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route("/unauthorized", methods=["GET"], strict_slashes=False)
def unauthorized() -> str:
    """
    GET /api/v1/unauthorized
    Triggers a 401 Unauthorized error.

    Returns:
        - Raises a 401 error with a description.
    """
    abort(401, description="Unauthorized")


@app_views.route("/forbidden", methods=["GET"], strict_slashes=False)
def forbidden() -> str:
    """
    GET /api/v1/forbidden
    Triggers a 403 Forbidden error.

    Returns:
        - Raises a 403 error with a description.
    """
    abort(403, description="Forbidden")


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status() -> str:
    """
    GET /api/v1/status
    Checks the status of the API.

    Returns:
        - JSON response with API status.
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats/", strict_slashes=False)
def stats() -> str:
    """
    GET /api/v1/stats
    Retrieves the count of various objects in the system.

    Returns:
        - JSON response containing the count of users.
    """
    from models.user import User

    stats = {"users": User.count()}
    return jsonify(stats)
