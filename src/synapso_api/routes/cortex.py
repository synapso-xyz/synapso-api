from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from synapso_core import CortexManager

from ..models import (
    Cortex,
    CreateCortexRequest,
    CreateCortexResponse,
    GetCortexResponse,
    ListCortexResponse,
)

router = APIRouter(tags=["cortex"])


@router.post(
    "/create",
    response_model=CreateCortexResponse,
    status_code=HTTPStatus.CREATED,
)
async def create_cortex(
    request: CreateCortexRequest, cortex_manager: CortexManager = Depends(CortexManager)
):
    created_cortex = cortex_manager.create_cortex(request.name, request.path)
    return CreateCortexResponse(cortex=Cortex.from_db_cortex(created_cortex))


@router.get(
    "",
    response_model=GetCortexResponse,
    status_code=HTTPStatus.OK,
)
async def get_cortex(
    cortex_id: Optional[str] = Query(None, description="The ID of the cortex"),
    cortex_name: Optional[str] = Query(None, description="The name of the cortex"),
    cortex_manager: CortexManager = Depends(CortexManager),
):
    if cortex_id:
        cortex = cortex_manager.get_cortex_by_id(cortex_id)
    elif cortex_name:
        cortex = cortex_manager.get_cortex_by_name(cortex_name)
    else:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Either cortex_id or cortex_name must be provided",
        )

    return GetCortexResponse(cortex=Cortex.from_db_cortex(cortex))


@router.get("/list", response_model=ListCortexResponse, status_code=HTTPStatus.OK)
async def list_cortex(cortex_manager: CortexManager = Depends(CortexManager)):
    cortices = cortex_manager.list_cortices()
    return ListCortexResponse(
        cortices=[Cortex.from_db_cortex(cortex) for cortex in cortices]
    )


@router.post("/index", status_code=HTTPStatus.OK)
async def index_cortex(
    cortex_id: Optional[str] = Query(None, description="The ID of the cortex"),
    cortex_name: Optional[str] = Query(None, description="The name of the cortex"),
    cortex_manager: CortexManager = Depends(CortexManager),
):
    if not cortex_id and not cortex_name:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Either cortex_id or cortex_name must be provided",
        )

    result = cortex_manager.index_cortex(cortex_id, cortex_name)
    if result:
        return {"message": "Cortex indexed successfully"}
    else:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Failed to index cortex: {str(result) if hasattr(result, '__str__') else 'Unknown error'}",
        )
