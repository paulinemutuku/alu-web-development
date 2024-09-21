#!/usr/bin/env python3
""" Module of Session Authentication
"""

from api.v1.views import app_views
from flask import request, abort
from models.user import User
from flask import jsonify
import os


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login() -> str:
    """POST /api/v1/auth_session/login
    Return:
    - session ID
    """
    email = request.form.get("email")

    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        found_user_bool = user.is_valid_password(password)
        if user.is_valid_password(password):
            found_user = user
    if not found_user_bool:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth

    session_id = auth.create_session(found_user.id)
    session_name = os.getenv("SESSION_NAME")
    response = jsonify(found_user.to_json())
    response.set_cookie(session_name, session_id)
    return response


@app_views.route("/auth_session/logout",
                 methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """DELETE /api/v1/auth_session/logout
    Return:
    - empty JSON
    """
    from api.v1.app import auth

    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200
