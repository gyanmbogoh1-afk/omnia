from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI(title="OMNIA Streaming API", version="0.1.0")


@app.get("/stream")
async def stream_demo() -> StreamingResponse:
    async def generator():
        for token in ["OMNIA", " is", " working", " on", " your", " request."]:
            yield token

    return StreamingResponse(generator(), media_type="text/plain")
