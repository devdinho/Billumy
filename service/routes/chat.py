from fastapi import APIRouter, Request, Header, HTTPException, Depends
from fastapi.responses import StreamingResponse

from models.chat import ChatCreate, ChatInDB, ChatUpdate, GenTitle

from db.mongo import chat_collection

from typing import AsyncGenerator, Optional
from datetime import datetime
import httpx
import os

router = APIRouter(prefix="/chats", tags=["Chats"])

billumy_url = os.getenv("BILLUMY_URL", "http://billumy:11414")
LLM_URL = "{}/api/chat".format(billumy_url)

@router.post("/", response_model=ChatInDB)
async def create_chat(chat: ChatCreate):
    chat_db = ChatInDB(user_id=chat.user_id, data=chat.data)
    await chat_collection.insert_one(chat_db.dict(by_alias=True))
    return chat_db

@router.get("/{chat_id}", response_model=ChatInDB)
async def get_chat(chat_id: str):
    result = await chat_collection.find_one({"id": chat_id})
    if not result:
        raise HTTPException(status_code=404, detail="Chat não encontrado")
    return ChatInDB(**result)

@router.patch("/{chat_id}/title")
async def update_chat_title(chat_id: str):
    chat = await chat_collection.find_one({"id": chat_id})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat não encontrado")
    
    messages = chat.get("data", {}).get("messages", [])
    user_message = next((m.get('content') for m in messages if m.get('role') == "user"), "Chat sem título")
    
    title = await GenTitle(user_message, f'{billumy_url}/api/generate')

    await chat_collection.update_one(
        {"id": chat_id},
        {"$set": {"title": title, "updated_at": datetime.utcnow()}}
    )

    return {"chat_id": chat_id, "title": title}


@router.post("/chat/stream")
async def stream_chat(request: Request, authorization: Optional[str] = Header(None)):
    body = await request.json()

    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json"
    }

    async def llm_response_stream() -> AsyncGenerator[str, None]:
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", LLM_URL, json=body, headers=headers) as response:
                async for chunk in response.aiter_text():
                    yield chunk

    return StreamingResponse(llm_response_stream(), media_type="text/plain")

@router.put("/{chat_id}/update")
async def update_chat(
    chat_id: str,
    update: ChatUpdate,
):
    chat = await chat_collection.find_one({"id": chat_id})
    
    if not chat:
        raise HTTPException(status_code=404, detail="Chat não encontrado")

    result = await chat_collection.update_one(
        {"id": chat_id},
        {
            "$set": {
                "data": update.data.dict(),
                "updated_at": datetime.utcnow()
            }
        }
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Nenhuma atualização realizada")

    return {"status": "updated", "chat_id": chat_id}