from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from src.graph.graph import runnable
from src.state.state import AgentState
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage
from pydantic import BaseModel
from typing import List

app = FastAPI()

class ChatInput(BaseModel):
    user_query: str
    history: List[dict] = [] # Added for chat history

origins = [
    "http://localhost:5500", # Allow local development UI
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/ui", StaticFiles(directory="ui"), name="ui")
templates = Jinja2Templates(directory="ui")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(input_data: ChatInput):
    user_query = input_data.user_query
    
    # Convert history from dict to BaseMessage objects
    converted_history = []
    for msg in input_data.history:
        if msg["type"] == "human":
            converted_history.append(HumanMessage(content=msg["content"]))
        elif msg["type"] == "ai":
            converted_history.append(AIMessage(content=msg["content"]))
    
    # Combine historical messages with the current user query
    inputs = {"messages": converted_history + [HumanMessage(content=user_query)], "user_query": user_query}
    
    response = runnable.invoke(inputs) # type: ignore
    return {"response": response["messages"][-1].content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
