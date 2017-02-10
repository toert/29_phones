from sqlalchemy import Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import sessionmaker
from os import getenv

TABLES_TO_CLONE = ['orders']


def make_session(db_uri):
    engine = create_engine(db_uri, echo=False, convert_unicode=True)
    session_class = sessionmaker(bind=engine)
    return session_class(), engine


def quick_mapper(table_name):
    base = declarative_base()

    class GenericMapper(base):
        __table__ = table_name

    return GenericMapper


def pull_data(from_db_uri, to_db_uri, tables):
    source, sengine = make_session(from_db_uri)
    smeta = MetaData(bind=sengine)
    destination, dengine = make_session(to_db_uri)

    for table_name in tables:
        table = Table(table_name, smeta, autoload=True)
        table.metadata.create_all(dengine)
        new_record = quick_mapper(table)
        columns = table.columns.keys()
        for record in source.query(table).all():
            all_columns_of_row = dict(
                [(str(column), getattr(record, column)) for column in columns]
            )
            destination.merge(new_record(**all_columns_of_row))
    destination.commit()


if __name__ == "__main__":
    pull_data(getenv('SRC_DB_URI'),
              getenv('FINAL_DB_URI'),
              TABLES_TO_CLONE)
