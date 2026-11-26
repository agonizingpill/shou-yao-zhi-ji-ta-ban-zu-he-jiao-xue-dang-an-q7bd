from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.looms_model import looms
from domain.segments_model import segments
from domain.axes_model import axes
from domain.lesson_demos_model import lesson_demos


def fit_axes(conn, user, data):
    segment = get(conn, segments, data.segment)
    archive = [x for x in scan(conn, segments) if x['loom'] == segment['loom']
               and x['checked'] and x['code'] != data.segment]
    need(segment['checked'], '待辨样段未经对拍')
    need(all(sum(x['pattern']==kind for x in archive)>=4 for kind in ('平纹','斜纹','缎纹')),
         '同台织架的三类参考样段不足')
    return submit(user, {'target':segment,'archive':archive})


def record_axis(conn, user, data):
    run = result(user, data.token)
    target = run['input']['target']
    stats = run['result']
    need(get(conn, segments, target['code']) == target, '样段快照已变化')
    need(stats['holdout_accuracy'] >= .66 and stats['confidence'] >= .55, '判别置信度不足，保留原示范')
    return insert(conn, axes, code=data.code, segment=target['code'], suggestion=stats['label'],
                  confidence=stats['confidence'],holdout=stats['holdout_accuracy'], token=data.token)
