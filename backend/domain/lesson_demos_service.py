from core.records import get, insert, need, scan, update
from domain.looms_model import looms
from domain.segments_model import segments
from domain.axes_model import axes
from domain.lesson_demos_model import lesson_demos


def replace_demo(conn, user, data):
    previous = get(conn, lesson_demos, data.previous, lock=True)
    loom = get(conn, looms, data.loom, lock=True)
    axis = get(conn, axes, data.axis)
    get(conn, segments, axis['segment'])
    need(previous['lesson'] == data.lesson and previous['state'] in ('旧示范','当前示范'), '节次或版本无法替换')
    need(loom['mapping_signed'], '目标织架脚位映射尚未签约')
    need(axis['state'] == '有效', '判别签注已作废或待复核，不能据此替换示范')
    row = insert(conn, lesson_demos, code=data.code, axis=data.axis, loom=data.loom,
                 lesson=data.lesson, state='当前示范', replaced_from=data.previous)
    update(conn, lesson_demos, data.previous, state='已被替换')
    return row


def restore_demo(conn, user, data):
    keys = sorted({data.demo,data.older})
    need(len(keys) == 2, '两个示范编号须不同')
    rows = {key:get(conn, lesson_demos, key, lock=True) for key in keys}
    latest, old = rows[data.demo], rows[data.older]
    need(latest['state'] not in ('已停用',), '已停用的示范须人工复核，不能直接退回')
    need(latest['lesson'] == old['lesson'] and latest['state']=='当前示范' and old['state']=='已被替换',
         '待撤回与被替换的示范须来自同一节次')
    old_axis = get(conn, axes, old['axis'])
    need(old_axis['state'] == '有效', '旧示范的判别签注已作废或待复核，不能退回')
    update(conn, lesson_demos, data.demo, state='已撤回')
    return update(conn, lesson_demos, data.older, state='当前示范')
