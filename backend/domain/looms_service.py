from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.looms_model import looms
from domain.segments_model import segments
from domain.axes_model import axes
from domain.lesson_demos_model import lesson_demos


def sign_mapping(conn, user, data):
    row = get(conn, looms, data.loom, lock=True)
    need(len(data.mapping_note) >= 7 and '双签' in data.mapping_note, '脚位图尚缺两位技师凭据')
    return update(conn, looms, row['code'], mapping_signed=True)
