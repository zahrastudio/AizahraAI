# chat_ws.py (skeleton)
from fastapi import FastAPI, WebSocket
app = FastAPI()

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        data = await ws.receive_text()
        # panggil model chat (OpenAI) -> response_text
        await ws.send_text(response_text)

