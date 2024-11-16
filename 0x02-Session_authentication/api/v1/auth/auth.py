#!/usr/bin/env python3
"""
definition of the class Auth
"""
import os
from flask import request
from typing import (
    List,
    TypeVar
)


class Auth:
    """
    managing API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        determineing whether given path requiring authentication or not
        Args->
             path(str): Url path to be checked
             excluded_paths(List of str): list of paths which donot require
              authentication
        Return->
            True if path is not in excluded_paths and else is False
        """
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        returning authorization header from request object
        """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returning User instance from information which comes from request object
        """
        return None

    def session_cookie(self, request=None):
        """
        returning cookie from request
        Args->
            request : request object
        Return->
            the value of _my_session_id cookie from the request object
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
