from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


segments = Table('segments', metadata,
    Column('code', String(64), primary_key=True),
    Column('loom', String(160), ForeignKey('looms.code'), nullable=False),
    Column('pattern', String(160), nullable=False),
    Column('right_rate', Float, nullable=False),
    Column('left_rate', Float, nullable=False),
    Column('pause', Float, nullable=False),
    Column('checked', Boolean, nullable=False),
    Column('revoked', Boolean, nullable=False, server_default='0'),
    Column('revoked_at', DateTime, nullable=True),
    CheckConstraint('right_rate >= 0'),
    CheckConstraint('left_rate >= 0'),
    CheckConstraint('pause >= 0'),
)


# 签注与计算所用样段的来源台账：待辨/训练/留出都登记，供撤销对拍时追溯
axis_lineages = Table('axis_lineages', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('axis', String(64), ForeignKey('axes.code'), nullable=False, index=True),
    Column('segment', String(64), ForeignKey('segments.code'), nullable=False, index=True),
    Column('role', String(16), nullable=False),
    CheckConstraint("role in ('target','train','holdout')"),
)


# 撤销对拍事件与影响快照；同一节次重复撤销按事件重放，不重复回退
revocations = Table('revocations', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('segment', String(64), ForeignKey('segments.code'), nullable=False),
    Column('actor', String(100), nullable=False),
    Column('at', DateTime, nullable=False),
    Column('impact', JSON, nullable=False),
)
