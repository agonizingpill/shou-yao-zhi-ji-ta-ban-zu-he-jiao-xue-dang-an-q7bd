import json
from sqlalchemy import func, select

from core.db import transaction
from domain.demo import FIXTURES
from domain.learning import calculate
from domain.segments_model import axis_lineages

def seed():
    sizes = {}
    with transaction() as conn:
        rows_by_code = {}
        for table, rows in FIXTURES:
            for row in rows:
                present = conn.scalar(select(table.c.code).where(table.c.code == row['code']))
                if present is None:
                    conn.execute(table.insert().values(**row))
                rows_by_code.setdefault(table.name, {})[row['code']] = row
            sizes[table.name] = conn.scalar(select(func.count()).select_from(table))

        # 为种子签注补齐样段来源台账（待辨/训练/留出），与真实计算保持一致
        existing_lineage = conn.scalar(select(func.count()).select_from(axis_lineages))
        if not existing_lineage:
            segments_by_code = rows_by_code['segments']
            for axis in rows_by_code['axes'].values():
                target = segments_by_code[axis['segment']]
                archive = [seg for code, seg in segments_by_code.items() if code != target['code']
                           and seg['loom'] == target['loom']]
                stats = calculate({'target': target, 'archive': archive})
                held_out = {item['code'] for item in stats['held_out_segments']}
                conn.execute(axis_lineages.insert().values(
                    axis=axis['code'], segment=target['code'], role='target'))
                for sample in archive:
                    conn.execute(axis_lineages.insert().values(
                        axis=axis['code'], segment=sample['code'],
                        role='holdout' if sample['code'] in held_out else 'train'))
            sizes['axis_lineages'] = conn.scalar(select(func.count()).select_from(axis_lineages))
    return sizes

if __name__ == '__main__':
    print(json.dumps(seed(), ensure_ascii=False, sort_keys=True))
