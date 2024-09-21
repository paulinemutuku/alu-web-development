#!/usr/bin/env python3


"""
Auth class
"""
from flask import request
from api.v1.views import app_views
from models.user import User
from typing import List, TypeVar
import os


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require Auth"""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != "/":
            path = path + "/"
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar("User"):
        """Current user"""
        return

    def session_cookie(self, request=None):
        """Session cookie"""
        if request is None:
            return None
        return request.cookies.get(os.getenv("SESSION_NAME"), None)
