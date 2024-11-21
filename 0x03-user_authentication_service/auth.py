#!/usr/bin/env python3
"""
 The authentication module
"""
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """ The auth class for interacting with authentication database
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ registering the new user
            Args->
                 email = the user's email
                 password = the user's password
            Return->
                 the User instance which is created
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            user = db.add_user(email, _hash_password(password))
            return user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """ checking if the password is valid
            Args->
                 email = the user's email
                 password = the user's password
            Return->
                 true if the credentials are valid and otherwise False
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            return False
        if not bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            return False
        return True

    def create_session(self, email: str) -> str:
        """ creating the session for the user
            Args->
                 email = the user's email
            Return->
                 the created session_id
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """ getting the user based on their session id
            Args->
                 session_id = the user's session_id
            Return->
                 the User if it found else none
        """
        if not session_id:
            return None
        db = self._db
        try:
            user = db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """ destroying the user session
        """
        db = self._db
        db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ generating the reset password token for the valid user
            Args->
                 email = the user's email
            Return->
                 the reset password token
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ updating the password for the user with matching the reset token
            Args->
                 reset_toke = the user's reset token
                 password = new password
            Return->
                 none
        """
        db = self._db
        try:
            user = db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        db.update_user(user.id, hashed_password=_hash_password(password),
                       reset_token=None)


def _hash_password(password: str) -> bytes:
    """ creating the password hash
        Args->
             password = user password
        Return->
            the hashed password
    """
    e_pwd = password.encode()
    return bcrypt.hashpw(e_pwd, bcrypt.gensalt())


def _generate_uuid() -> str:
    """ generating the unique ids
        Return->
             the UUID which is generated
    """
    return str(uuid4())
