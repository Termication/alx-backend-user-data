#!/usr/bin/env python3
"""
API entry point module.
Sets up the application, registers routes, handles authentication, 
and defines error handlers.
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
import os

# Initialize Flask application
app = Flask(__name__)

# Register blueprints for routing
app.register_blueprint(app_views)

# Enable CORS for all routes starting with '/api/v1/*'
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Authentication setup based on environment variable
auth = None
AUTH_TYPE = os.getenv("AUTH_TYPE")

if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth

    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth

    auth = BasicAuth()


@app.before_request
def before_request_handler():
    """
    Process each request before it reaches the route handler.
    If authentication is enabled, check for valid authorization headers.
    """
    if auth is not None:
        # List of routes that do not require authentication
        excluded_routes = [
            "/api/v1/status/",
            "/api/v1/unauthorized/",
            "/api/v1/forbidden/",
        ]

        # Check if the current route requires authentication
        if auth.require_auth(request.path, excluded_routes):
            # Abort with a 401 error if the Authorization header is missing
            if auth.authorization_header(request) is None:
                abort(401, description="Unauthorized")
            # Abort with a 403 error if the user is not authenticated
            if auth.current_user(request) is None:
                abort(403, description="Forbidden")


@app.errorhandler(404)
def not_found(error) -> str:
    """Handle 404 errors (Not Found)."""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Handle 401 errors (Unauthorized)."""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Handle 403 errors (Forbidden)."""
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    # Get host and port from environment variables or use default values
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
