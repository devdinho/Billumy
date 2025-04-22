from fastapi import FastAPI
from routes import chat
from dotenv import load_dotenv

import os
import httpx

load_dotenv()

app = FastAPI()
app.include_router(chat.router)

billumy_url = os.getenv("BILLUMY_URL", "http://billumy:11414")
 
@app.get("/")
async def billumy_healthcheck():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{billumy_url}")
        if response.status_code == 200:
            return {"status": "Billumy is up 🚀"}
        else:
            return {"status": "error", "message": response.text}