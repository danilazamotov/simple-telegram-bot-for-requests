import pytz
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.testing.plugin.plugin_base import logging

from database.DatabaseConfig import Requests


class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.Session = config.Session

    def add_request(self, manager_id, manager_name, phone_request, payment_date, currency, amount, payment_to_whom,
                    purpose_of_payment, payment_format, due_date, payment_recipient_name=None,
                    payment_phone_number=None, date_created=None, status_to_send=False, director_approval=None,
                    accounting_approval=None):
        request_id = None
        session = self.Session()
        if date_created is None:
            date_created = str(datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M'))
        try:
            new_request = Requests(
                manager_id=manager_id,
                manager_name=manager_name,
                phone_request=phone_request,
                payment_date=payment_date,
                currency=currency,
                amount=amount,
                payment_to_whom=payment_to_whom,
                purpose_of_payment=purpose_of_payment,
                payment_format=payment_format,
                due_date=due_date,
                status_to_send=status_to_send,
                payment_recipient_name=payment_recipient_name,
                payment_phone_number=payment_phone_number,
                director_approval=director_approval,
                accounting_approval=accounting_approval,
                date_created=date_created
            )
            session.add(new_request)
            session.commit()
            request_id = new_request.id
        except SQLAlchemyError as e:
            session.rollback()
            logging(e)
            return request_id
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