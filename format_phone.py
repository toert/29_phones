import re
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import sessionmaker, load_only

engine = create_engine(getenv('FINAL_DB_URI'))
metadata = MetaData(bind=engine, reflect=True)
base = declarative_base(bind=engine, metadata=metadata)
session = sessionmaker(engine)()


class Orders(base):
    __tablename__ = 'orders'


def format_phone(entry_phone, result_phone_lenght=10):
    phone_without_symbols = ''.join(re.findall(r'\d', entry_phone))
    return phone_without_symbols[-result_phone_lenght:]


def fill_new_column():
    all_orders_from_db = session.query(Orders).options(load_only('id', 'contact_phone')).all()
    objects = (
        dict(
            id=order.id,
            formatted_contact_phone=format_phone(order.contact_phone)
        )
        for order in all_orders_from_db
    )
    session.bulk_update_mappings(Orders, objects)
    session.commit()


if __name__ == "__main__":
    fill_new_column()
