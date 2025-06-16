from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import openai, os, asyncio

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    messages = body.get("messages", [])

    async def stream():
        resp = openai.ChatCompletion.create(
            model="gpt-4o", messages=messages, stream=True
        )
        for chunk in resp:
            delta = chunk["choices"][0]["delta"].get("content", "")
            if delta:
                yield f"data: {delta}\n\n"
            await asyncio.sleep(0)

    headers = {
        "x-vercel-ai-data-stream": "v1",
        "Content-Type": "text/event-stream"
    }
    return StreamingResponse(stream(), headers=headers, media_type="text/event-stream")
