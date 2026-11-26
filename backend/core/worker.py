import json
from pathlib import Path
from traceback import print_exc

from sqlalchemy import select

from core.db import transaction
from core.queueing import QUEUE, broker
from domain.learning import calculate
from domain.segments_model import segments

pulse = Path('/tmp/compute-heartbeat')

def _still_valid(job_input):
    """计算落库前再核对一次：撤销对拍的样段不得参与计算。"""
    used = [job_input.get('target', {})] + list(job_input.get('archive', []))
    codes = [item['code'] for item in used if item.get('code')]
    if not codes:
        return False, '计算输入缺少样段'
    with transaction() as conn:
        rows = conn.execute(select(segments).where(segments.c.code.in_(codes))).mappings().all()
    if len(rows) != len(codes):
        return False, '计算所用样段已不存在'
    revoked = [row['code'] for row in rows if row['revoked'] or not row['checked']]
    if revoked:
        return False, f'计算所用样段 {revoked[0]} 已撤销对拍或未对拍'
    return True, ''

def serve():
    while True:
        broker.ping()
        pulse.touch()
        item = broker.blmove(QUEUE, f'{QUEUE}:processing', timeout=2, src='LEFT', dest='RIGHT')
        if item is None:
            continue
        job = json.loads(item)
        status = {'owner': job['owner'], 'input': job['input']}
        try:
            valid, reason = _still_valid(job['input'])
            if not valid:
                raise ValueError(reason)
            status.update(status='ready', result=calculate(job['input']))
        except ValueError as exc:
            status.update(status='rejected', detail=str(exc))
        except Exception:
            print_exc()
            status.update(status='rejected', detail='计算失败，请检查输入和 worker 日志')
        with broker.pipeline() as pipe:
            pipe.set(f'compute:{job["token"]}', json.dumps(status, allow_nan=False), ex=86400)
            pipe.lrem(f'{QUEUE}:processing', 1, item)
            pipe.execute()
        pulse.touch()

if __name__ == '__main__':
    for raw in broker.lrange(f'{QUEUE}:processing', 0, -1):
        with broker.pipeline() as pipe:
            pipe.lpush(QUEUE, raw)
            pipe.lrem(f'{QUEUE}:processing', 1, raw)
            pipe.execute()
    serve()
