from fastapi import APIRouter, Request, Header, HTTPException, Depends
from fastapi.responses import StreamingResponse

from models.chat import ChatCreate, ChatInDB, ChatUpdate

from db.mongo import chat_collection

from typing import AsyncGenerator, Optional
from dotenv import load_dotenv
from datetime import datetime
import httpx
import os

load_dotenv()

billumy_url = os.getenv("BILLUMY_URL", "http://billumy:11414")

LLM_URL = "{}/api/chat".format(billumy_url)

BILLUMY_API_KEY = os.getenv("BILLUMY_API_KEY", "insecure_token")

def verificar_token(authorization: str = Header(...)):
    if authorization != f"Bearer {BILLUMY_API_KEY}":
        raise HTTPException(status_code=401, detail="Token inválido")
    
router = APIRouter(prefix="/chats", tags=["Chats"], dependencies=[Depends(verificar_token)])


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


@router.put("/{chat_id}/update")
async def update_chat(
    chat_id: str,
    update: ChatUpdate,
):
    chat = await chat_collection.find_one({"id": chat_id})
    
    if not chat:
        raise HTTPException(status_code=404, detail="Chat não encontrado")

    update_fields = {
        "data": update.data.dict(),
        "updated_at": datetime.now()
    }

    if update.title:
        update_fields["title"] = update.title

    result = await chat_collection.update_one(
        {"id": chat_id},
        {"$set": update_fields}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Nenhuma atualização realizada")

    return {"status": "updated", "chat_id": chat_id}


@router.post("/title")
async def generate_chat_title(request: Request, authorization: Optional[str] = Header(None)):
    body = await request.json()

    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json"
    }
    
    llm_url = f"{billumy_url}/api/generate"
    
    return StreamingResponse(llm_response_stream(body=body, headers=headers, llm_url=llm_url), media_type="text/plain")


@router.post("/stream")
async def stream_chat(request: Request, authorization: Optional[str] = Header(None)):
    body = await request.json()

    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json"
    }
    
    return StreamingResponse(llm_response_stream(body=body, headers=headers), media_type="text/plain")

async def llm_response_stream(body, headers, llm_url=LLM_URL) -> AsyncGenerator[str, None]:
    async with httpx.AsyncClient() as client:
        async with client.stream("POST", llm_url, json=body, headers=headers) as response:
            async for chunk in response.aiter_text():
                yield chunk