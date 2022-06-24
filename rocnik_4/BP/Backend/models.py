from xmlrpc.client import Boolean
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from database import Base
import datetime


class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True)
    value_oxy = Column(Integer)
    value_bpm = Column(Integer)
    temp_obj = Column(Float)
    temp_amp = Column(Float)
    datetime = Column(DateTime, default=datetime.datetime.utcnow)


    def __init__(self, value_oxy=None, value_bpm=None, temp_obj=None, temp_amp=None):
        self.value_oxy = value_oxy
        self.value_bpm = value_bpm
        self.temp_obj = temp_obj
        self.temp_amp = temp_amp


class Pressure(Base):
    __tablename__ = "pressures"
    id = Column(Integer, primary_key=True)
    dia = Column(Integer)
    pulz = Column(Integer)
    sys = Column(Float)
    datetime = Column(DateTime)
    


    def __init__(self, dia=None, pulz=None, sys=None, datetime=None):
        self.dia = dia
        self.pulz = pulz
        self.sys = sys
        self.datetime = datetime


