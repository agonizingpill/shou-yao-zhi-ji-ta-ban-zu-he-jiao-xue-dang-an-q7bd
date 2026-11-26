from core.queueing import submit, result
from core.records import get, insert, need, scan
from domain.segments_model import axis_lineages, segments
from domain.axes_model import axes


def fit_axes(conn, user, data):
    segment = get(conn, segments, data.segment)
    need(segment['checked'] and not segment['revoked'], '待辨样段未经对拍或已撤销')
    archive = [x for x in scan(conn, segments) if x['loom'] == segment['loom']
               and x['checked'] and not x['revoked'] and x['code'] != data.segment]
    need(all(sum(x['pattern']==kind for x in archive)>=4 for kind in ('平纹','斜纹','缎纹')),
         '同台织架的三类参考样段不足')
    return submit(user, {'target':segment,'archive':archive})


def record_axis(conn, user, data):
    run = result(user, data.token)
    need(run['status'] == 'ready', '计算未完成，不能签注')
    target = run['input']['target']
    archive = run['input']['archive']
    stats = run['result']

    # 撤销对拍后排队任务会被置为拒绝；这里再兜底拦截，保证任何用过该样段的任务都不能签注
    current_target = get(conn, segments, target['code'])
    need(not current_target['revoked'], '待辨样段已撤销对拍，该计算不得签注')
    need(current_target == target, '样段快照已变化')
    for sample in archive:
        current = get(conn, segments, sample['code'])
        need(not current['revoked'], f'参考样段 {sample["code"]} 已撤销对拍，该计算不得签注')
        need(current == sample, '参考样段快照已变化')
    need(stats['holdout_accuracy'] >= .66 and stats['confidence'] >= .55, '判别置信度不足，保留原示范')

    row = insert(conn, axes, code=data.code, segment=target['code'], suggestion=stats['label'],
                 confidence=stats['confidence'], holdout=stats['holdout_accuracy'],
                 token=data.token, state='有效')
    # 登记样段来源：待辨、训练、留出都算，供撤销对拍时追溯
    insert(conn, axis_lineages, axis=data.code, segment=target['code'], role='target')
    held_out = {item['code'] for item in stats.get('held_out_segments', [])}
    for sample in archive:
        insert(conn, axis_lineages, axis=data.code, segment=sample['code'],
               role='holdout' if sample['code'] in held_out else 'train')
    return row
