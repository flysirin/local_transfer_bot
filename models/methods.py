from typing import List, Type
from sqlalchemy import create_engine, and_, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import count
from datetime import datetime

from models.create_db import Drivers, Users, BannedUsers, Orders, Admin, OrderStatus

engine = create_engine('sqlite:///users_sqlite.db')


def database_action(func):
    def wrapper(*args, **kwargs):
        session = Session(bind=engine)
        try:
            result = func(session, *args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    return wrapper


@database_action
def create_order(session: Session, user_id, username, location_id) -> None:
    existing_user = session.query(Users).filter_by(user_id=user_id).first()
    user = Users(user_id=user_id, username=username, location_id=location_id)
    order = Orders(user_id=user_id, username=username, location_id=location_id)

    if not existing_user:
        session.add(user)
    else:
        session.query(Users).filter_by(user_id=user_id).update({'location_id': location_id})
    session.add(order)


@database_action
def add_admin_to_db(session: Session, username: str, admin_id: int = None) -> None:
    admin = Admin(username=username)
    if session.query(Admin).filter_by(username=username).first():
        session.close()
        return
    session.add(admin)


@database_action
def add_admin_id_to_db(session: Session, username: str, admin_id: int):
    session.query(Admin).filter_by(username=username, admin_user_id=None).update({'admin_user_id': admin_id})


@database_action
def remove_admin_from_db(session: Session, username: str) -> None:
    session.query(Admin).filter_by(username=username).delete()


@database_action
def add_driver_to_db(session: Session, username: str) -> None:
    driver = Drivers(username=username)
    if session.query(Drivers).filter_by(username=username).first():
        session.close()
        return
    session.add(driver)


@database_action
def get_driver_usernames_from_db(session: Session) -> list[str]:
    drivers_obj = session.query(Drivers).all()
    drivers_usernames = [driver_id.username for driver_id in drivers_obj]
    return drivers_usernames


@database_action
def add_driver_id(session: Session, driver_id: int, username: str) -> None:
    session.query(Drivers).filter_by(username=username).update({'driver_id': driver_id,
                                                                'is_available': True})


@database_action
def delete_driver(session: Session, username: str) -> None:
    session.query(Drivers).filter_by(username=username).delete()


@database_action
def get_location_id_from_user_id(session: Session, user_id: int) -> int:
    location_id = session.query(Users).filter_by(user_id=user_id).first()
    if location_id:
        return location_id.location_id


@database_action
def get_free_driver_id_from_db(session: Session) -> int:
    driver = (session.query(Drivers.driver_id, count(Orders.date_create))
                    .outerjoin(Orders, (Orders.driver_id == Drivers.driver_id) & (Drivers.is_available == 1))
                    .group_by(Drivers.driver_id)
                    .order_by(count(Orders.date_create))
                    .first())
    if driver:
        return driver[0]


@database_action
def get_banned_users(session: Session) -> list[int]:
    banned_users = session.query(BannedUsers).all()
    banned_users_ids = [banned_user.user_id for banned_user in banned_users]
    return banned_users_ids


@database_action
def get_free_orders(session: Session) -> list[Type[Orders]]:
    orders = session.query(Orders).filter_by(status_drive=OrderStatus.FIND.value).all()
    return orders


@database_action
def get_free_order_by_user(session: Session, user_id) -> bool:
    order = session.query(Orders).filter_by(user_id=user_id).order_by(desc(Orders.date_create)).first()
    if order.status_drive == OrderStatus.FIND.value:
        return True


@database_action
def get_confirmed_orders(session: Session) -> list[Type[Orders]]:
    orders = session.query(Orders).filter_by(status_drive=OrderStatus.DRIVE.value).all()
    return orders


@database_action
def update_order_status(session: Session, user_id: int, status_drive: str, driver_id: int = None) -> None:
    last_order = session.query(Orders).filter_by(user_id=user_id, driver_id=driver_id).order_by(
        desc(Orders.date_create)).first()
    last_order.status_drive = status_drive


@database_action
def put_driver_to_order(session: Session, user_id: int, status_drive: str, driver_id: int = None) -> None:
    last_order = session.query(Orders).filter_by(user_id=user_id).order_by(
        desc(Orders.date_create)).first()
    last_order.status_drive = status_drive
    last_order.driver_id = driver_id


@database_action
def get_admins(session: Session) -> list[str]:
    admins = session.query(Admin).all()
    admin_usernames = [admin_username.username for admin_username in admins]
    return admin_usernames


@database_action
def stat_orders(session: Session) -> str:
    orders = (session.query(Orders.username, Drivers.username, Orders.date_create, Orders.status_drive)
              .outerjoin(Drivers, Orders.driver_id == Drivers.driver_id)
              .order_by(desc(Orders.date_create))
              .all())
    result = ''
    status_emo: dict = {OrderStatus.FIND.value: '🔎', OrderStatus.DRIVE.value: '🚕', OrderStatus.END.value: '✅'}

    for order in orders:
        username, driver_name, date, status = order
        result += f'🧑{username}🚓{driver_name}🕐{date.strftime("%d %H:%M")}-{status_emo.get(status, None)}\n'
    return result
