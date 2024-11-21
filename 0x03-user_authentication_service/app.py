#!/usr/bin/env python3
"""
Flask app providing user authentication routes.
"""
from flask import Flask, request, jsonify, abort, redirect, url_for
from auth import Auth

app = Flask(__name__)
AUTH = Auth()

# Index Route
@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    Return a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


# User Registration Route
@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """
    Register a new user with email and password.
    Returns:
        - 201: User successfully created.
        - 400: Email already registered.
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"})


# User Login Route
@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    Log in a user and create a session.
    Returns:
        - 200: Login successful with session cookie.
        - 401: Invalid login credentials.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    resp = jsonify({"email": email, "message": "logged in"})
    resp.set_cookie("session_id", session_id)
    return resp


# User Logout Route
@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """
    Log out a user and destroy their session.
    Returns:
        - 302: Redirect to the home page after logout.
        - 403: Session ID is invalid or not found.
    """
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None or session_id is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


# Profile Route
@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
    Retrieve a user's email based on their session ID.
    Returns:
        - 200: User email.
        - 403: Invalid or missing session ID.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


# Generate Reset Password Token Route
@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    Generate a reset token for a user's password.
    Returns:
        - 200: Token successfully generated.
        - 403: User email not found.
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token})


# Update Password Route
@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    Update a user's password using their reset token.
    Returns:
        - 200: Password updated successfully.
        - 403: Invalid reset token or user email.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"})


# Main Entry Point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
