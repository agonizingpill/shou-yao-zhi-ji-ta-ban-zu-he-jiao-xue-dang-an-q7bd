from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import looms_service as service
from domain.looms_model import looms
from domain.looms_schemas import SignMapping

router = APIRouter()

@router.get('/looms')
def list_looms(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, looms)


@router.post('/looms/sign-mapping')
def sign_mapping(data: SignMapping, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.sign_mapping(conn, user, data)
        record(conn, user, 'looms.sign_mapping')
        return output
