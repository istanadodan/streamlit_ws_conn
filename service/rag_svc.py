import requests
from streamlit.runtime.uploaded_file_manager import UploadedFile
from schemas.query import QueryByRagRequest
from core.config import settings


def call_rag_api(message: str, top_k: int, llm: str, retriever: str):
    endpoint = f"{settings.rag_api_url}/app/query_by_rag"
    data = QueryByRagRequest(
        query=message, top_k=top_k, llm=llm, retriever=retriever
    ).model_dump(by_alias=True)

    response = requests.post(endpoint, json=data)
    if response.status_code != 200:
        return dict(answer=f"Error: {response.reason}")

    return response.json()["result"]


def call_rag_pipeline_api(upload_file: UploadedFile):
    endpoint = f"{settings.rag_api_url}/app/rag-pipeline"
    files = {
        "upload_file": (upload_file.name, upload_file.getvalue(), upload_file.type)
    }

    response = requests.post(endpoint, files=files)
    if response.status_code != 200:
        return dict(answer=f"Error: {response.reason}")

    return response.json()["result"]
