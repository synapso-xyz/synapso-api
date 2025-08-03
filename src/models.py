from typing import List

from pydantic import BaseModel, Field
from synapso_core.data_store.data_models import DBCortex


class SynapsoRequest(BaseModel):
    pass


class SynapsoResponse(BaseModel):
    pass


class Cortex(BaseModel):
    id: str = Field(..., description="The ID of the cortex")
    name: str = Field(..., description="The name of the cortex")
    path: str = Field(..., description="The path to the cortex")

    @classmethod
    def from_db_cortex(cls, db_cortex: DBCortex) -> "Cortex":
        return cls(
            id=db_cortex.cortex_id,
            name=db_cortex.cortex_name,
            path=db_cortex.path,
        )


class CreateCortexRequest(SynapsoRequest):
    name: str = Field(..., description="The name of the cortex")
    path: str = Field(..., description="The path to the cortex")


class CreateCortexResponse(SynapsoResponse):
    cortex: Cortex = Field(..., description="The cortex that was created")


class GetCortexResponse(SynapsoResponse):
    cortex: Cortex = Field(..., description="The cortex that was retrieved")


class ListCortexResponse(SynapsoResponse):
    cortices: List[Cortex] = Field(..., description="The list of cortices")


class QueryRequest(SynapsoRequest):
    query: str = Field(..., description="The query to be executed")


class QueryResponse(SynapsoResponse):
    result: str = Field(..., description="The result of the query")
    time_taken: float = Field(
        ..., description="The time taken in seconds to execute the query"
    )
