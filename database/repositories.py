from database.models import Users, Transmissions
from database.session import SessionFactoryPool


class RepositoryBase:
    """
    Base class for repository classes. This attempts to implement all base CRUD operations for easy extension. The
    constructor takes a parameter `use_new_session: bool` to determine whether a new session should be created while
    instantiating the repo object.

    The intended use of this base class is by extending it and specifying a `__model_type__` class member. This variable
    is required and must be set to the SQLAlchemy Model class (for now, only `declarative_base` is supported. Also, for
    now, the primary key column for the tables must be `id`.

    The simplest usage example is:

    ```python
    class SomeEntityRepository(RepositoryBase):
        __model_type__ = SomeEntity


    repo = SomeEntityRepository()
    entity = repo.get(1)
    ```
    """
    __model_type__ = None

    def __init__(self, use_new_session=False):
        if use_new_session:
            self._session = SessionFactoryPool.create_new_session()
        else:
            self._session = SessionFactoryPool.get_current_session()

    def all(self):
        """
        A simple SELECT * function

        :return: A list of all entities in the database
        """
        # TODO Add pagination
        return self._create_query().all()

    def create(self, entity):
        """
        Persists an object in the database. Generates a new id if not explicitly specified.

        :param entity: The entity object to persist.
        """
        self._session.add(entity)
        self._session.commit()

    def get(self, identifier):
        """
        Fetches an entity with the given identifier.

        :param identifier: The primary key of the entity to fetch
        :return: The entity or None
        """
        return self.filter_by(self.__model_type__.id == identifier).first()

    def update(self, identity, **kwargs):
        """
        Updates an already generated entity.

        :param identity: The entity to update
        :param kwargs: Field names that are to be updated
        """
        # FIXME This should be more secure
        for key in kwargs:
            value = kwargs[key]
            if value is not None and hasattr(identity, key):
                setattr(identity, key, value)

        self._session.commit()

    def delete(self, entity):
        """
        Drops an entity from the database

        :param entity: The entity to delete
        """
        _entity = self.get(entity.id)
        self._session.delete(_entity)
        self._session.commit()

    def filter_by(self, criterion):
        """
        Generates an SQLAlchemy filter based on the specified criteria.

        :param criterion: The `BinaryExpression` criteria to filter by
        :return: A filtered result set
        """
        return self._create_query().filter(criterion)

    def _create_query(self):
        return self._session.query(self.__model_type__)


class UserRepository(RepositoryBase):
    __instance = None
    __model_type__ = Users

    @staticmethod
    def get_instance():
        if UserRepository.__instance is None:
            UserRepository.__instance = UserRepository()

        return UserRepository.__instance

    def get_by_username(self, username):
        return self.filter_by(self.__model_type__.username == username).first()

    def get_by_access_key(self, access_key):
        return self.filter_by(self.__model_type__.access_key == access_key).frist()


class TransmissionRepository(RepositoryBase):
    __instance = None
    __model_type__ = Transmissions

    @staticmethod
    def get_instance():
        if TransmissionRepository.__instance is None:
            TransmissionRepository.__instance = TransmissionRepository()

        return TransmissionRepository.__instance

    def get_by_transmission_key(self, transmission_key):
        return self.filter_by(self.__model_type__.transmission_key == transmission_key).first()

    def get_by_user_id(self, user_id):
        return self.filter_by(self.__model_type__.user_id == user_id).first()
