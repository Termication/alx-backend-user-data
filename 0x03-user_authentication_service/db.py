#!/usr/bin/env python3
"""
Database Module for managing User objects.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """
    A database interface for managing User objects.
    Handles user creation, querying, and updating.
    """

    def __init__(self) -> None:
        """
        Initialize the database connection and schema.
        Creates a SQLite database and initializes the User table.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)  # Clear existing schema
        Base.metadata.create_all(self._engine)  # Create new schema
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Lazy initialization of a SQLAlchemy session.
        Ensures that the session is only created once and reused.
        Returns:
            Session: SQLAlchemy session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.
        Args:
            email (str): The email address of the user.
            hashed_password (str): The hashed password of the user.
        Returns:
            User: The newly created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Retrieve a user by matching attributes.
        Args:
            **kwargs: Arbitrary keyword arguments representing user attributes to filter by.
        Returns:
            User: The user matching the specified attributes.
        Raises:
            InvalidRequestError: If an invalid attribute is provided.
            NoResultFound: If no user matches the criteria.
        """
        for key in kwargs:
            if key not in User.__dict__:
                raise InvalidRequestError(f"Invalid attribute: {key}")

        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound(f"No user found matching: {kwargs}")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes in the database.
        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments representing the attributes to update.
        Raises:
            ValueError: If the user is not found or an invalid attribute is provided.
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError(f"User with ID {user_id} not found.")

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError(f"Invalid attribute: {key}")

        self._session.commit()
