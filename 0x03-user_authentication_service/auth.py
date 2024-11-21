#!/usr/bin/env python3
"""
Authentication module: provides functions and classes to handle user authentication,
password hashing, session management, and password reset functionality.
"""
import bcrypt
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar, Union

from db import DB
from user import User

U = TypeVar(User)


def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt and return the hashed password.
    Args:
        password (str): Plain-text password to be hashed.
    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generate a unique UUID as a string.
    Returns:
        str: A new UUID as a string.
    """
    return str(uuid4())


class Auth:
    """
    Auth class to manage user authentication and session operations.
    Provides functionality to register users, validate logins, manage sessions,
    and handle password resets.
    """

    def __init__(self) -> None:
        """
        Initialize the Auth class with a database connection.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user in the database.
        Args:
            email (str): Email address of the user.
            password (str): Plain-text password of the user.
        Returns:
            User: The newly created user object.
        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate user login credentials.
        Args:
            email (str): User's email address.
            password (str): User's plain-text password.
        Returns:
            bool: True if credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Union[None, str]:
        """
        Create a session for a user and return the session ID.
        Args:
            email (str): User's email address.
        Returns:
            str: The session ID if the user exists, or None otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[None, U]:
        """
        Retrieve a user based on their session ID.
        Args:
            session_id (str): The session ID of the user.
        Returns:
            User: The user object if found, or None otherwise.
        """
        if not session_id:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a user's session by setting their session ID to None.
        Args:
            user_id (int): ID of the user whose session is to be destroyed.
        Returns:
            None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a password reset token for a user.
        Args:
            email (str): User's email address.
        Returns:
            str: The generated reset token.
        Raises:
            ValueError: If the user does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError("User not found")

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update a user's password using a valid reset token.
        Args:
            reset_token (str): Token issued for password reset.
            password (str): New plain-text password for the user.
        Returns:
            None
        Raises:
            ValueError: If the reset token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password, reset_token=None)
        except NoResultFound:
            raise ValueError("Invalid reset token")
