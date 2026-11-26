from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


axes = Table('axes', metadata,
    Column('code', String(64), primary_key=True),
    Column('segment', String(160), ForeignKey('segments.code'), nullable=False),
    Column('suggestion', String(160), nullable=False),
    Column('confidence', Float, nullable=False),
    Column('holdout', Float, nullable=False),
    Column('token', String(64), nullable=False, unique=True),
    # 有效：可作示范依据；已作废：撤销对拍牵连；待复核：旧签注查不清样段来源
    Column('state', String(16), nullable=False, server_default='有效'),
    CheckConstraint('holdout between 0 and 1'),
    CheckConstraint('confidence between 0 and 1'),
    CheckConstraint("state in ('有效','已作废','待复核')"),
)
