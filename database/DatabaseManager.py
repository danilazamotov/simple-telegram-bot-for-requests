import pytz
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.testing.plugin.plugin_base import logging

from database.DatabaseConfig import Requests


class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.Session = config.Session

    def add_request(self, **kwargs):
        session = self.Session()
        request_id = None
        if 'date_created' not in kwargs:
            kwargs['date_created'] = datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
        try:
            new_request = Requests(**kwargs)
            session.add(new_request)
            session.commit()
            request_id = new_request.id
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Error adding request: {e}")
        finally:
            session.close()
        return request_id

    def update_request_approval(self, request_id, approval, role):
        session = self.Session()
        try:
            request = session.query(Requests).filter_by(id=request_id).one()
            if role == 'manager':
                request.status_to_send = approval
            elif role == 'director':
                request.director_approval = approval
            elif role == 'accountant':
                request.accounting_approval = approval
            session.commit()
            return True
        except NoResultFound:
            logging.error(f"Request with id {request_id} not found.")
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Error updating request approval: {e}")
        finally:
            session.close()
        return False

    def get_request_data_by_id(self, request_id):
        session = self.Session()
        try:
            request = session.query(Requests).filter_by(id=request_id).one()
            return {
                "manager_id": request.manager_id,
                "manager_name": request.manager_name,
                "phone_request": request.phone_request,
                "payment_date": request.payment_date,
                "currency": request.currency,
                "amount": request.amount,
                "payment_to_whom": request.payment_to_whom,
                "purpose_of_payment": request.purpose_of_payment,
                "payment_format": request.payment_format,
                "payment_phone_number": request.payment_phone_number or '',
                "payment_recipient_name": request.payment_recipient_name or '',
                "due_date": request.due_date
            }
        except NoResultFound:
            logging.error(f"Request with id {request_id} not found.")
            return None
        except SQLAlchemyError as e:
            logging.error(f"Error retrieving request data: {e}")
            return None
        finally:
            session.close()

    def get_unapproved_requests_first(self, person):
        session = self.Session()
        try:
            if person == 'director':
                request = session.query(Requests).filter(
                    Requests.director_approval == None,
                    Requests.status_to_send == True
                ).first()
            elif person == 'accountant':
                request = session.query(Requests).filter(
                    Requests.accounting_approval == None,
                    Requests.director_approval == 'подтверждено'
                ).first()
            else:
                request = None
            return request
        except SQLAlchemyError as e:
            logging.error(f"Error retrieving unapproved requests: {e}")
            return None
        finally:
            session.close()