from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.looms_model import looms
from domain.segments_model import segments
from domain.axes_model import axes
from domain.lesson_demos_model import lesson_demos


def record_segment(conn, user, data):
    get(conn, looms, data.loom)
    need(data.pattern in ('平纹','斜纹','缎纹'), '须选用三种课堂纹样词表')
    need(0 <= data.right_rate <= 10 and 0 <= data.left_rate <= 10 and .1 <= data.pause <= 5,
         '课上踏板频次或停顿超出记录范围')
    return insert(conn, segments, **data.model_dump(), checked=False)


def verify_segment(conn, user, data):
    get(conn, segments, data.segment, lock=True)
    return update(conn, segments, data.segment, checked=True)
