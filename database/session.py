from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from constants import constants
from database.models import Base as DeclarativeBase

SQLITE_FILE = f"sqlite:///{constants.work_dir}/owncloud.db"


class SessionFactoryPool:
    """
    This class provides easy methods to obtain the current open or an entirely
    new database session.
    """
    current_session = None

    @staticmethod
    def get_current_session():
        """
        Returns the current active database session. Opens a new one if a
        session isn't running.
        :return: Current database session
        """
        if SessionFactoryPool.current_session is None:
            session = SessionFactoryPool.create_new_session()
            SessionFactoryPool.current_session = session

        return SessionFactoryPool.current_session

    @staticmethod
    def create_new_session():
        """
        Creates a new database session.
        :return: A new database session
        """
        database_engine = create_engine(SQLITE_FILE)
        DeclarativeBase.metadata.create_all(database_engine)
        DeclarativeBase.bind = database_engine

        session = sessionmaker()
        session.configure(bind=database_engine)

        return session()
