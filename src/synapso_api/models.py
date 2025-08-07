from typing import List

from pydantic import BaseModel, Field
from synapso_core.data_store.data_models import DBCortex


class SynapsoRequest(BaseModel):
    """
    Base request model for all Synapso API requests.
    """

    pass


class SynapsoResponse(BaseModel):
    """
    Base response model for all Synapso API responses.
    """

    pass


class Cortex(BaseModel):
    """
    Cortex model.
    """

    id: str = Field(..., description="The ID of the cortex")
    name: str = Field(..., description="The name of the cortex")
    path: str = Field(..., description="The path to the cortex")

    @classmethod
    def from_db_cortex(cls, db_cortex: DBCortex) -> "Cortex":
        """
        Create a Cortex model from a DBCortex object.
        """
        return cls(
            id=db_cortex.cortex_id,
            name=db_cortex.cortex_name,
            path=db_cortex.path,
        )


class CreateCortexRequest(SynapsoRequest):
    """
    Request model for creating a cortex.
    """

    name: str = Field(..., description="The name of the cortex")
    path: str = Field(..., description="The path to the cortex")


class CreateCortexResponse(SynapsoResponse):
    """
    Response model for creating a cortex.
    """

    cortex: Cortex = Field(..., description="The cortex that was created")


class GetCortexResponse(SynapsoResponse):
    """
    Response model for getting a cortex.
    """

    cortex: Cortex = Field(..., description="The cortex that was retrieved")


class ListCortexResponse(SynapsoResponse):
    """
    Response model for listing cortices.
    """

    cortices: List[Cortex] = Field(..., description="The list of cortices")


class QueryRequest(SynapsoRequest):
    """
    Request model for querying a cortex.
    """

    query: str = Field(..., description="The query to be executed")


class QueryResponse(SynapsoResponse):
    """
    Response model for querying a cortex.
    """

    result: str = Field(..., description="The result of the query")
    time_taken: float = Field(
        ..., description="The time taken in seconds to execute the query"
    )
