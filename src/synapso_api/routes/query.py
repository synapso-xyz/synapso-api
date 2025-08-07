import time
from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from synapso_core.query_manager import QueryManager

from ..models import QueryRequest, QueryResponse

router = APIRouter(tags=["query"])


@router.post("/query", status_code=HTTPStatus.OK, response_model=QueryResponse)
async def query(
    request: QueryRequest,
    query_manager: QueryManager = Depends(QueryManager),
):
    """
    Query a cortex (non-streaming)
    """
    time_start = time.time()
    result = query_manager.query(request.query)
    time_end = time.time()
    return QueryResponse(
        result=result,
        time_taken=time_end - time_start,
    )


@router.post("/query_stream", status_code=HTTPStatus.OK)
async def stream_query(
    request: QueryRequest,
    query_manager: QueryManager = Depends(QueryManager),
):
    """
    Query a cortex (streaming)
    """
    result_stream = query_manager.query_stream(request.query)
    return StreamingResponse(result_stream, media_type="text/plain")
