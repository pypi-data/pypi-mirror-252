import json
from time import perf_counter
from fastapi import FastAPI, WebSocket, Response as FastAPIResponse
from starlette.websockets import WebSocketDisconnect, WebSocketState
from listen.Wav2Vec.engine import Transcriber, Response, Error
from listen.Wav2Vec import utils
from listen.exception import NotAllowedToListenError

CONFIG = utils.get_config_or_default()
is_allowed_to_listen = utils.is_allowed_to_listen(CONFIG)

if not is_allowed_to_listen:
    raise NotAllowedToListenError(utils.CONFIG_PATH)

models_path = utils.get_loc_model_path()

print("Loading transcription model...")
transcriber = Transcriber(models_path=models_path)

print("Starting server...")
app = FastAPI()

@app.get("/")
async def healthcheck():
    """
    Health check endpoint
    """
    return FastAPIResponse(content="Welcome to listen.sock: Transcription as a Service!", status_code=200)

@app.websocket("/api/v2/transcribe")
async def transcribe(websocket: WebSocket):
    """
    Transcribe audio data received via WebSocket
    """
    print("Received WebSocket request at /api/v2/transcribe")
    await websocket.accept()
    try:
        while True:
            audio_data = await websocket.receive_bytes()
            inference_start = perf_counter()
            text, _ = transcriber.run(audio_data)
            inference_end = perf_counter() - inference_start
            print(f"Completed WebSocket request at /api/v2/transcribe in {inference_end} seconds")
            await websocket.send_json(json.dumps(Response(text, inference_end).__dict__))
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_json(json.dumps(Error(str(e)).__dict__))

