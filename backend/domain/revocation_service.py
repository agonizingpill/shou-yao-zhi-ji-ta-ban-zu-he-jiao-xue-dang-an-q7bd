import json
import logging
from datetime import datetime, timezone

from redis.exceptions import RedisError
from sqlalchemy import select

from core.queueing import QUEUE, broker
from core.records import get, need, scan, update
from domain.axes_model import axes
from domain.lesson_demos_model import lesson_demos
from domain.segments_model import axis_lineages, revocations, segments


def revoke_segment(conn, user, data):
    """复核员撤销样段对拍。

    - 用过该样段的判别签注全部作废（待辨、训练、留出都算）；查不清来源的旧签注转待复核。
    - 受牵连的在用示范沿替换记录退到最近的有效版本，找不到就停用。
    - 排队计算用过该样段的任务置为拒绝，使其无法再签注。
    同一节次重复撤销返回已登记的影响快照，不重复回退。
    """
    segment = get(conn, segments, data.segment, lock=True)

    # 重试撤销：按已登记事件重放影响快照，不重复回退
    existing = conn.execute(
        select(revocations).where(revocations.c.segment == data.segment)
        .order_by(revocations.c.id)).mappings().all()
    if existing:
        return {'segment': data.segment, 'replayed': len(existing),
                'impact': existing[-1]['impact']}

    need(segment['checked'] and not segment['revoked'], '样段未对拍或已撤销，无法撤销对拍')

    update(conn, segments, data.segment, checked=False, revoked=True,
           revoked_at=datetime.now(timezone.utc))

    lineage_rows = conn.execute(
        select(axis_lineages).where(axis_lineages.c.segment == data.segment)).mappings().all()
    affected_codes = sorted({row['axis'] for row in lineage_rows})
    all_axes = scan(conn, axes)
    linked = {row['code']: row for row in all_axes if row['code'] in affected_codes}

    # 没有来源台账的旧签注查不清用过哪些样段，转待复核，不参与回退
    pending = [row['code'] for row in all_axes
               if row['state'] == '有效' and not conn.execute(
                   select(axis_lineages.c.id).where(axis_lineages.c.axis == row['code']).limit(1)).first()]
    for code in pending:
        update(conn, axes, code, state='待复核')
    for code in affected_codes:
        update(conn, axes, code, state='已作废')

    blocked_tokens = _block_queued_computes(conn, data.segment)

    lessons = []
    for demo in scan(conn, lesson_demos):
        if demo['state'] != '当前示范' or demo['axis'] not in linked:
            continue
        outcome = _rollback_demo(conn, demo)
        lessons.append(outcome)

    impact = {
        'voided_axes': sorted(linked),
        'pending_axes': sorted(pending),
        'blocked_tokens': blocked_tokens,
        'lessons': lessons,
    }
    result = conn.execute(revocations.insert().values(
        segment=data.segment, actor=user['sub'],
        at=datetime.now(timezone.utc), impact=impact))
    return {'segment': data.segment, 'replayed': 0,
            'revocation_id': result.inserted_primary_key[0], 'impact': impact}


def _rollback_demo(conn, current):
    """受牵连的当前示范沿替换链退到最近的有效版本，找不到则停用。"""
    trail = [current['code']]
    predecessor_code = current['replaced_from']
    seen = {current['code']}
    while predecessor_code and predecessor_code not in seen:
        candidate = get(conn, lesson_demos, predecessor_code)
        trail.append(predecessor_code)
        axis = get(conn, axes, candidate['axis'])
        if candidate['state'] in ('旧示范', '已被替换') and axis['state'] == '有效':
            update(conn, lesson_demos, current['code'], state='已撤回')
            update(conn, lesson_demos, candidate['code'], state='当前示范')
            return {'lesson': current['lesson'], 'demo': current['code'],
                    'outcome': 'rolled_back', 'restored': candidate['code'],
                    'original_axis': current['axis'], 'trail': trail}
        seen.add(predecessor_code)
        predecessor_code = candidate['replaced_from']
    update(conn, lesson_demos, current['code'], state='已停用')
    return {'lesson': current['lesson'], 'demo': current['code'],
            'outcome': 'deactivated', 'restored': None,
            'original_axis': current['axis'], 'trail': trail}


def _block_queued_computes(conn, segment_code):
    """排队中的计算任务若用过该样段（待辨或参考），置为拒绝，杜绝再签注。

    排队期 compute:{token} 仅存状态，输入保存在队列项里，因此同时扫描队列与处理中队列。
    代理不可用时不阻断撤销：worker 落库前校验与签注前快照校验仍会拦下受影响任务。
    """
    tokens = []
    try:
        queued_items = {}
        for queue_name in (QUEUE, f'{QUEUE}:processing'):
            for raw in broker.lrange(queue_name, 0, -1):
                try:
                    item = json.loads(raw)
                except (TypeError, json.JSONDecodeError):
                    continue
                queued_items[item['token']] = (queue_name, raw, item)

        for token, (queue_name, raw, item) in queued_items.items():
            status_key = f'compute:{token}'
            status_raw = broker.get(status_key)
            if status_raw is None:
                continue
            record = json.loads(status_raw)
            if record.get('status') != 'queued':
                continue
            payload = item.get('input', {})
            used = [payload.get('target', {})] + list(payload.get('archive', []))
            if not any(entry.get('code') == segment_code for entry in used):
                continue
            record['status'] = 'rejected'
            record['detail'] = f'计算所用样段 {segment_code} 已撤销对拍，任务不得签注'
            record['input'] = payload
            broker.set(status_key, json.dumps(record, ensure_ascii=False), ex=86400)
            # 同步更新队列项，避免 worker 取到旧输入后重新计算
            updated = json.dumps(item, ensure_ascii=False)
            broker.lrem(queue_name, 1, raw)
            broker.rpush(queue_name, updated)
            tokens.append(token)
    except RedisError:
        logging.getLogger('uvicorn.error').exception(
            '计算代理不可用，排队任务拦截降级，样段 %s 的撤销仍已落库', segment_code)
    return sorted(tokens)


def list_revocations(conn):
    rows = conn.execute(select(revocations).order_by(revocations.c.id)).mappings().all()
    return [dict(row) for row in rows]
