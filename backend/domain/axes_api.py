from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import axes_service as service
from domain.axes_model import axes
from domain.axes_schemas import FitAxes, RecordAxis

router = APIRouter()

@router.get('/axes')
def list_axes(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, axes)


@router.post('/axes/fit-axes')
def fit_axes(data: FitAxes, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.fit_axes(conn, user, data)
        record(conn, user, 'axes.fit_axes')
        return output


@router.post('/axes/record-axis')
def record_axis(data: RecordAxis, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.record_axis(conn, user, data)
        record(conn, user, 'axes.record_axis')
        return output
