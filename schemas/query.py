from pydantic import BaseModel, Field


class QueryByRagRequest(BaseModel):
    query: str
    top_k: int = 3
    llm: str = ""
    retriever: str = "qdrant"
    filter: dict[str, str] = Field(
        default_factory=dict,
        examples=[{"producer": "ESP Ghostscript 7.07"}],
    )
