import re
import time
from os import getenv
from sqlalchemy.exc import DBAPIError
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


def fill_formatted_phone_column(orders):
    objects = (
        dict(
            id=order.id,
            formatted_contact_phone=format_phone(order.contact_phone)
        )
        for order in orders
    )
    session.bulk_update_mappings(Orders, objects)
    session.commit()


if __name__ == "__main__":
    while True:
        try:
            raw_orders_query = session.query(Orders).options(load_only('id', 'contact_phone')).filter(Orders.formatted_contact_phone.is_(None))
            fill_formatted_phone_column(raw_orders_query.yield_per(getenv('MAX_LOADED_ROWS_AMOUNT')))
            time.sleep(getenv('SLEEP_TIME'))
        except KeyboardInterrupt:
            print('Exit was initialized by user')
            break
        except DBAPIError:
            print('Lost connection, next try after {} seconds'.format(getenv('SLEEP_TIME')))
            session.rollback()
            time.sleep(getenv('SLEEP_TIME'))
