import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker


from entity import *

class Schedule:
  def __init__( self, db_filename ):
    self.db_filename = db_filename

    self.engine = sqlalchemy.create_engine('sqlite:///%s' % self.db_filename, echo=False)

    Base.metadata.bind = self.engine

    Base.metadata.autoflush = False
    Base.metadata.autocommit = False

    Session = scoped_session(sessionmaker())
    Base.query = Session.query_property()
    self.session = Session()

  @property
  def routes(self):
    return self.session.query(Route).all()

  @property
  def agencies(self):
    return self.session.query(Agency).all()

  @property
  def service_periods(self):
    return self.session.query(ServicePeriod).all()

  @property
  def stops(self):
    return self.session.query(Stop).all()

  @property
  def trips(self):
    return self.session.query(Trip).all()

  def service_for_date(self, service_date):
    active_periods = []
    for period in self.service_periods:
      if period.active_on_date(service_date):
        active_periods.append(period)
    return active_periods

  def create_tables( self ):
    Base.metadata.create_all()
    self.session.commit()
