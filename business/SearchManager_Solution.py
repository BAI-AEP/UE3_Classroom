import os
from pathlib import Path

from data_access.data_base import init_db
from sqlalchemy import select, func, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from data_models.models import *


class SearchManager(object):
    def __init__(self) -> None:
        self.__load_db()

    def __load_db(self):
        # Ensure the environment Variable is set
        db_file = os.environ.get('DB_FILE')  # Lesen einer Umgebungsvariable

        if not db_file:
            raise ValueError("You have to define the environment variable 'DB_FILE'")
        self.__db_filepath = Path(db_file)

        # Ensure the db file exists, if not create a new db file with or without example data
        # You have to delete the db file, if you need a new fresh db.
        if not self.__db_filepath.is_file():
            init_db(db_file, generate_example_data=True)

        # create the engine and the session.
        # the engine is private, no need for subclasses to be able to access it.
        self._engine = create_engine(f'sqlite:///{db_file}')
        # create the session as db connection
        # subclasses need access therefore, protected attribute so every inheriting manager has access to the connection
        self._session = scoped_session(sessionmaker(bind=self._engine))

    def get_all_hotels(self):
        query = select(Hotel)
        return self._session.execute(query).scalars().all()

    def get_hotels_by_city(self, city: str):
        query = select(Hotel).join(Address).where(Address.city == city)
        return self._session.execute(query).scalars().all()


if __name__ == '__main__':
    # This is only for testing without Application

    # You should set the variable in the run configuration
    # Because we are executing this file in the folder ./business/
    # we need to relatively navigate first one folder up and therefore,
    # use ../data in the path instead of ./data
    # if the environment variable is not set, set it to a default
    if not os.environ.get('DB_FILE'):
        os.environ['DB_FILE'] = '../data/test.db'
    search_manager = SearchManager()
    all_hotels = search_manager.get_all_hotels()
    for hotel in all_hotels:
        print(hotel)

    city_user = input('City: ')
    hotels = search_manager.get_hotels_by_city(city_user)
    for hotel in hotels:
        print(hotel)
