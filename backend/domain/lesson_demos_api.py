from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import lesson_demos_service as service
from domain.lesson_demos_model import lesson_demos
from domain.lesson_demos_schemas import ReplaceDemo, RestoreDemo

router = APIRouter()

@router.get('/lesson_demos')
def list_lesson_demos(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, lesson_demos)


@router.post('/lesson_demos/replace-demo')
def replace_demo(data: ReplaceDemo, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.replace_demo(conn, user, data)
        record(conn, user, 'lesson_demos.replace_demo')
        return output


@router.post('/lesson_demos/restore-demo')
def restore_demo(data: RestoreDemo, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.restore_demo(conn, user, data)
        record(conn, user, 'lesson_demos.restore_demo')
        return output
