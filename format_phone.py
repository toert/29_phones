import re
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import sessionmaker

engine = create_engine(getenv('FINAL_DB_URI'))
metadata = MetaData(bind=engine, reflect=True)
base = declarative_base(bind=engine, metadata=metadata)
session_maker = sessionmaker(engine)
session = session_maker()


class Orders(base):
    __tablename__ = 'orders'


def format_phone(entry_phone, result_phone_lenght=10):
    phone_without_symbols = ''.join(re.findall(r'\d', entry_phone))
    return phone_without_symbols[-result_phone_lenght:]


def fill_new_column():
    for row in session.query(Orders).all():
        row.formatted_contact_phone = format_phone(row.contact_phone)
        session.add(row)
        session.commit()


if __name__ == "__main__":
    fill_new_column()
