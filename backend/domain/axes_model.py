from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


axes = Table('axes', metadata,
    Column('code', String(64), primary_key=True),
    Column('segment', String(160), ForeignKey('segments.code'), nullable=False),
    Column('suggestion', String(160), nullable=False),
    Column('confidence', Float, nullable=False),
    Column('holdout', Float, nullable=False),
    Column('token', String(64), nullable=False, unique=True),
    CheckConstraint('holdout between 0 and 1'),
    CheckConstraint('confidence between 0 and 1'),
)
