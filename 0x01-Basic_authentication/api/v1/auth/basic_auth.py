#!/usr/bin/env python3
"""
Defines the BasicAuth class for implementing Basic Authentication.
"""
import base64
from .auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic Authentication class implementing specific authentication methods."""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts the Base64 encoded part of the Authorization header.

        Args:
            authorization_header (str): The Authorization header value.

        Returns:
            str: The Base64 encoded string, or None if invalid.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        # Extract the token after "Basic "
        token = authorization_header.split(" ")[-1]
        return token

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        Decodes a Base64-encoded string.

        Args:
            base64_authorization_header (str): The Base64 string to decode.

        Returns:
            str: The decoded string, or None if decoding fails.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            encoded = base64_authorization_header.encode("utf-8")
            decoded = base64.b64decode(encoded)
            return decoded.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        Extracts user credentials (email and password) from a decoded Base64 string.

        Args:
            decoded_base64_authorization_header (str): The decoded Base64 string.

        Returns:
            tuple: A tuple containing the email and password, or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        email, password = decoded_base64_authorization_header.split(":", 1)
        return (email, password)

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """
        Retrieves a User instance based on email and password.

        Args:
            user_email (str): The user's email address.
            user_pwd (str): The user's password.

        Returns:
            User: The User object if authentication is successful, None otherwise.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar("User"):
        """
        Retrieves the current authenticated user based on the request.

        Args:
            request: The Flask request object.

        Returns:
            User: The authenticated User object, or None if authentication fails.
        """
        auth_header = self.authorization_header(request)
        if auth_header:
            token = self.extract_base64_authorization_header(auth_header)
            if token:
                decoded = self.decode_base64_authorization_header(token)
                if decoded:
                    email, password = self.extract_user_credentials(decoded)
                    if email:
                        return self.user_object_from_credentials(email, password)
        return None
