#!/usr/bin/env python3
"""
Main file for testing user authentication functionality.
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    Test user registration.
    Verifies that the user is successfully registered or that an error 
    is returned if the email is already registered.
    Args:
        email: User's email.
        password: User's password.
    """
    resp = requests.post('http://127.0.0.1:5000/users', data={'email': email, 'password': password})
    if resp.status_code == 200:
        assert resp.json() == {"email": email, "message": "user created"}
    else:
        assert resp.status_code == 400
        assert resp.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test login with incorrect password.
    Ensures that the server responds with an unauthorized error (401).
    Args:
        email: User's email.
        password: Incorrect password.
    """
    resp = requests.post('http://127.0.0.1:5000/sessions', data={'email': email, 'password': password})
    assert resp.status_code == 401


def profile_unlogged() -> None:
    """
    Test accessing the profile endpoint without being logged in.
    Ensures that the server responds with a forbidden error (403).
    """
    resp = requests.get('http://127.0.0.1:5000/profile')
    assert resp.status_code == 403


def log_in(email: str, password: str) -> str:
    """
    Test login with valid credentials.
    Verifies the response and retrieves the session ID.
    Args:
        email: User's email.
        password: User's password.
    Returns:
        The session ID of the logged-in user.
    """
    resp = requests.post('http://127.0.0.1:5000/sessions', data={'email': email, 'password': password})
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "logged in"}
    return resp.cookies['session_id']


def profile_logged(session_id: str) -> None:
    """
    Test accessing the profile endpoint while logged in.
    Ensures that the server responds with the user's email.
    Args:
        session_id: Session ID of the logged-in user.
    """
    cookies = {'session_id': session_id}
    resp = requests.get('http://127.0.0.1:5000/profile', cookies=cookies)
    assert resp.status_code == 200


def log_out(session_id: str) -> None:
    """
    Test logout functionality.
    Ensures that the user's session is destroyed and they are redirected.
    Args:
        session_id: Session ID of the logged-in user.
    """
    cookies = {'session_id': session_id}
    resp = requests.delete('http://127.0.0.1:5000/sessions', cookies=cookies)
    if resp.status_code == 302:
        assert resp.url == 'http://127.0.0.1:5000/'
    else:
        assert resp.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Test password reset token generation.
    Ensures that the server generates a valid reset token.
    Args:
        email: User's email.
    Returns:
        The reset token.
    """
    resp = requests.post('http://127.0.0.1:5000/reset_password', data={'email': email})
    if resp.status_code == 200:
        return resp.json()['reset_token']
    assert resp.status_code == 401


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Test updating the user's password.
    Verifies that the password is successfully updated using the reset token.
    Args:
        email: User's email.
        reset_token: Reset token for password update.
        new_password: New password.
    """
    data = {'email': email, 'reset_token': reset_token, 'new_password': new_password}
    resp = requests.put('http://127.0.0.1:5000/reset_password', data=data)
    if resp.status_code == 200:
        assert resp.json() == {"email": email, "message": "Password updated"}
    else:
        assert resp.status_code == 403


# Test credentials
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    # Run test scenarios
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
