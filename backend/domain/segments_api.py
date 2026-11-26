from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import segments_service as service
from domain.segments_model import segments
from domain.segments_schemas import RecordSegment, VerifySegment

router = APIRouter()

@router.get('/segments')
def list_segments(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, segments)


@router.post('/segments/record-segment')
def record_segment(data: RecordSegment, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.record_segment(conn, user, data)
        record(conn, user, 'segments.record_segment')
        return output


@router.post('/segments/verify-segment')
def verify_segment(data: VerifySegment, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.verify_segment(conn, user, data)
        record(conn, user, 'segments.verify_segment')
        return output
