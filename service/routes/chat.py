from fastapi import APIRouter, Request, Header, HTTPException, Depends
from fastapi.responses import StreamingResponse

from models.chat import ChatCreate, ChatInDB, ChatUpdate

from db.mongo import chat_collection

from typing import AsyncGenerator, Optional
from dotenv import load_dotenv
from datetime import datetime

import logging
import httpx
from httpx import ReadTimeout, RequestError

import os

load_dotenv()

logger = logging.getLogger(__name__)

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

    try:
        client = httpx.AsyncClient(timeout=httpx.Timeout(60.0))
        response = await client.post(LLM_URL, json=body, headers=headers)
        response.raise_for_status()
        await client.aclose()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erro ao contatar LLM: {str(e)}")

    return StreamingResponse(llm_response_stream(body=body, headers=headers), media_type="text/plain")


async def llm_response_stream(body, headers, llm_url=LLM_URL) -> AsyncGenerator[str, None]:
    timeout = httpx.Timeout(60.0)  # tempo aumentado para modelos demorados
    try:
        logger.info(f"Requisitando {llm_url}")
        async with httpx.AsyncClient(timeout=timeout) as client:
            async with client.stream("POST", llm_url, json=body, headers=headers) as response:
                response.raise_for_status()
                async for chunk in response.aiter_text():
                    yield chunk
    except ReadTimeout:
        logger.warning("Timeout na chamada ao LLM.")
        yield "[ERRO] Tempo de resposta do LLM esgotado.\n"
    except HTTPStatusError as e:
        logger.warning(f"Erro HTTP ao acessar o LLM: {e.response.status_code}")
        yield f"[ERRO] LLM retornou erro {e.response.status_code}.\n"
    except RequestError as e:
        logger.warning(f"Erro de requisição ao LLM: {str(e)}")
        yield f"[ERRO] Problema na comunicação com o LLM: {str(e)}\n"
    except Exception as e:
        logger.exception("Erro inesperado ao chamar o LLM")
        yield f"[ERRO] Erro inesperado: {str(e)}\n"