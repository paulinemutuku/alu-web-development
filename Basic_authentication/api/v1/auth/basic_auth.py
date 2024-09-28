#!/usr/bin/env python3
""" Module of Basic Auth
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic Auth class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract base64"""
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if authorization_header.startswith("Basic "):
            return authorization_header[6:]
        return None

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """Decode base64"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            return base64.b64decode(
                base64_authorization_header).decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """Extract user credentials"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) != str:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        user_pass = decoded_base64_authorization_header.split(":", 1)
        return user_pass[0], user_pass[1]

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """User object from credentials"""
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None
        from models.user import User

        try:
            user = User.search({"email": user_email})
            if len(user) == 0:
                return None
            user = user[0]
            if user.is_valid_password(user_pwd):
                return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Current user"""
        header = self.authorization_header(request)
        base64_auth = self.extract_base64_authorization_header(
            header)
        decoded_base64_auth = self.decode_base64_authorization_header(
            base64_auth)
        user_email, user_pwd = self.extract_user_credentials(
            decoded_base64_auth)
        return self.user_object_from_credentials(user_email, user_pwd)
