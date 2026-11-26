from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


looms = Table('looms', metadata,
    Column('code', String(64), primary_key=True),
    Column('machine', String(160), nullable=False),
    Column('pedal_count', Integer, nullable=False),
    Column('mapping_signed', Boolean, nullable=False),
    CheckConstraint('pedal_count between 2 and 12'),
)
