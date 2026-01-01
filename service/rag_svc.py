import requests
from schemas.query import QueryByRagRequest


def call_rag_api(message: str):
    url = "http://rag-api.local/rag-api/app/query_by_rag"
    data = QueryByRagRequest(query=message, top_k=3).model_dump(by_alias=True)
    response = requests.post(url, json=data)
    if response.status_code != 200:
        return dict(answer=f"Error: {response.reason}")
    return response.json()["result"]
