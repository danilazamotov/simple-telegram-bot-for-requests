from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Boolean


class DatabaseConfig:
    Base = declarative_base()

    def __init__(self, database_path):
        self.database_path = database_path
        self.engine = create_engine(f'sqlite:///{database_path}')
        self.Session = sessionmaker(bind=self.engine)

    def get_db_path(self):
        return self.database_path

    def initialize(self):
        self.Base.metadata.create_all(self.engine)


class Requests(DatabaseConfig.Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True)
    manager_id = Column(Integer, default=None)
    manager_name = Column(String, default=None)
    phone_request = Column(String, default=None)
    payment_date = Column(String, default=None)
    currency = Column(String, default=None)
    amount = Column(Integer, default=None)
    payment_to_whom = Column(String, default=None)
    purpose_of_payment = Column(String, default=None)
    payment_format = Column(String, default=None)
    due_date = Column(String, default=None)
    payment_recipient_name = Column(String, default=None)
    payment_phone_number = Column(String, default=None)

    status_to_send = Column(Boolean, default=False)
    director_approval = Column(String, default=None)
    accounting_approval = Column(String, default=None)

    date_created = Column(String, default=None)
