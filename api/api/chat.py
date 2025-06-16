from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import openai

app = FastAPI()

# CORS middleware (if frontend is hosted separately)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Chat API is working"}

@app.post("/chat")
async def chat(prompt: dict):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    messages = prompt.get("messages", [])
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or gpt-4 if you have access
        messages=messages
    )
    return {"response": response['choices'][0]['message']['content']}
