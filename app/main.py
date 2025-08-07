# main.py
import json
import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status
from pydantic import BaseModel
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

load_dotenv()




app = FastAPI()


from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Configuración de JWT ---
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"


# En un entorno de producción, esto debería estar en un archivo .env
N8N_WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Clase para gestionar las conexiones
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)

manager = ConnectionManager()

# --- Modelos Pydantic para el Webhook ---
class WebhookData(BaseModel):
    message: str
    sender_id: str
    recipient_id: str | None = None

# --- Endpoint de prueba ---
@app.get("/")
async def get_root():
    return {"message": "¡Servidor de chat corriendo!"}

# --- Endpoint de WebSocket con autenticación ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str):
    user_id: str | None = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise JWTError
    except JWTError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket, user_id)
    try:
        await manager.broadcast(f"El plomero con ID {user_id} se ha conectado.")
        while True:
            data = await websocket.receive_text()
            message_payload = {
                "sender_id": user_id,
                "message": data
            }

            # Envía el mensaje al webhook de n8n
            async with httpx.AsyncClient() as client:
                await client.post(N8N_WEBHOOK_URL, json=message_payload)

            await manager.broadcast(f"Plomero ({user_id}): {data}")
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        await manager.broadcast(f"El plomero con ID {user_id} se ha desconectado.")

# --- Endpoint para el webhook de n8n (simplificado) ---
@app.post("/webhook")
async def handle_webhook(data: WebhookData):
    print(f"Webhook recibido: {data.model_dump_json(indent=2)}")
    
    if data.recipient_id:
        await manager.send_personal_message(data.message, data.recipient_id)
    else:
        await manager.broadcast(data.message)

    return {"status": "ok", "message": "Mensaje procesado"}