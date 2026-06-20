# Create app/routers/policies.py
from fastapi import APIRouter, HTTPException

from app.schemas import Citation, PolicyRequest, PolicyResponse
from app.services import RAGService

router = APIRouter(prefix="/ai", tags=["AI Policies"])


@router.post("/ask-policy", response_model=PolicyResponse)
async def ask_policy_endpoint(request: PolicyRequest):
    try:
        from starlette.concurrency import run_in_threadpool

        # Offload the synchronous LlamaIndex call to a thread pool
        raw_response = await run_in_threadpool(
            RAGService._query_engine.query, request.question
        )

        citations_list = []

        for node in raw_response.source_nodes:
            citations_list.append(
                Citation(source_text=node.node.text[:200], relevance_score=node.score)
            )

        return PolicyResponse(answer=str(raw_response), citations=citations_list)

    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
