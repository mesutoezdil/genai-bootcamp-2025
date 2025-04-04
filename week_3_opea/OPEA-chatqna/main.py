from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from pydantic import BaseModel
import uvicorn

from chat import ChatConfig, QASystem

# Initialize FastAPI app
app = FastAPI(
    title="Chat QA System",
    description="A chat-based QA system using OpenAI's GPT models",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Initialize chat system
config = ChatConfig.from_env()
qa_system = QASystem(config)

class QuestionRequest(BaseModel):
    """Request model for questions."""
    question: str

@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    """Serve the chat interface."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/conversations")
async def create_conversation():
    """Create a new conversation."""
    conv_id = qa_system.create_conversation()
    return {"conversation_id": conv_id}

@app.post("/conversations/{conv_id}/question")
async def ask_question(conv_id: str, request: QuestionRequest):
    """Ask a question in a conversation."""
    try:
        answer = await qa_system.get_answer(conv_id, request.question)
        return {"answer": answer}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
