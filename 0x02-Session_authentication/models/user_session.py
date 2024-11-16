#!/usr/bin/env python3
""" the usersession module
"""
from models.base import Base


class UserSession(Base):
    """
    the UserSession class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        initializing the UserSession instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
