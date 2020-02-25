from datetime import datetime, date, time, timedelta
from sqlalchemy import create_engine, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://postgres:1234@127.0.0.1/dstubot')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

days_of_week = ('пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс')
days_of_week_enum = Enum(*days_of_week, name="days_of_week")
pairs_time = (time(8, 30), time(10, 15), time(12, 00), time(14, 15), time(16, 00), time(17, 45), time(19, 30))


def current_semester():
    month = datetime.now().month
    return 2 if (month >= 2 and not month >= 9) else 1


def current_week():
    a = date(datetime.now().year, 9, 1)
    offset = a.weekday() if a.weekday() < 6 else -1
    b = datetime.now().date()
    days = (b - a).days + offset
    return 1 if ((days // 7) % 2 == 0) else 2


from app.models.models_user import *
from app.models.models_faculty import *
from app.models.models_place import *
from app.models.models_other import *
from app.models.models_schedule import *

# Создание таблиц
Base.metadata.create_all(engine)