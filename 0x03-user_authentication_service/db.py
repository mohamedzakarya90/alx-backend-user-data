#!/usr/bin/env python3
""" The DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """ initializing new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """ The memorized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ creating the new User instances and
            saving them to database
            Args->
                 email
                 hashed_password
            Return->
                 the new User object
        """
        session = self._session
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            session.add(new_user)
            session.commit()
        except Exception:
            session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ finding the user by given attribute
            Args->
                  the dictionary of attributes for using as search
                  parameter
            Return->
                  the user object
        """

        attrs, vals = [], []
        for attr, val in kwargs.items():
            if not hasattr(User, attr):
                raise InvalidRequestError()
            attrs.append(getattr(User, attr))
            vals.append(val)

        session = self._session
        query = session.query(User)
        user = query.filter(tuple_(*attrs).in_([tuple(vals)])).first()
        if not user:
            raise NoResultFound()
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """ searching for the user instance which is using the given id parameter
            Args->
                 user_id: user's id
            Return->
                 the user instance which is found
        """
        user = self.find_user_by(id=user_id)
        session = self._session
        for attr, val in kwargs.items():
            if not hasattr(User, attr):
                raise ValueError
            setattr(user, attr, val)
        session.commit()
