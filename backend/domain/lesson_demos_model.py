from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


lesson_demos = Table('lesson_demos', metadata,
    Column('code', String(64), primary_key=True),
    Column('axis', String(160), ForeignKey('axes.code'), nullable=False),
    Column('loom', String(160), ForeignKey('looms.code'), nullable=False),
    Column('lesson', String(160), nullable=False),
    Column('state', String(160), nullable=False),
)
