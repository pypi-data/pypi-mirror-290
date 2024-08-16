import logging
import io
import json
import asyncio
import soundfile
from time import perf_counter
from fastapi import FastAPI, WebSocket, Request, Response as FastAPIResponse
from fastapi.responses import StreamingResponse, JSONResponse
from starlette.websockets import WebSocketDisconnect
from concurrent.futures import ThreadPoolExecutor
from say.TTS.engine import TTS, Response, Error, load_models
from say.TTS import utils
from say import MODEL_PATH, I18N

logging.info("Serving Speech from Text (Text-To-Speech)")

CONFIG = utils.get_config_or_default()

# Load app configs and initialize STT model
try:
    n_proc_available = CONFIG['service']['n_proc']
except Exception as e:
    logging.warning(f"Could not fetch key {e} from config.")
    nproc = utils.get_available_cpu_count() // 4 # 1/4 of available CPUs
    print(f"Using {nproc} worker{'s' if nproc > 1 else ''} instead.")
    n_proc_available = nproc

logging.info("Starting Server...")
executor = ThreadPoolExecutor(max_workers=n_proc_available)
app = FastAPI()

logging.info("Loading model...")

language = "EN_NEWEST" if I18N.lower() == 'en' else I18N.upper()
speaker = "en-newest" if I18N.lower() == 'en' else I18N.lower()
speaker_id = "EN-Newest" if I18N.lower() == 'en' else I18N.upper()

toneconverter, synthesizer, source_se = load_models(MODEL_PATH, language, speaker, ckpt_version=2.0)

engine = TTS(
    toneconverter,
    synthesizer,
    source_se,
)

@app.get("/")
async def healthcheck():
    return FastAPIResponse(content="Welcome to TTS.socket: Text-To-Speech as a Service!", status_code=200)

@app.websocket("/api/v1/tts")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_json('binary')
        except WebSocketDisconnect:
            break
        logging.info("Received websocket request at /api/v1/tts")
        # json_data = json.loads(data)
        logging.debug("With parameters:")
        logging.debug("%s", data)
        inference_start = perf_counter()
        wav = await asyncio.get_event_loop().run_in_executor(None, lambda: engine.run(data.get('text'), speaker_id, data.get('style_wav')))
        inference_end = perf_counter() - inference_start
        
        if isinstance(wav, Error):
            await websocket.send_json({"error": wav.message})
            continue
        # def stream_audio():
        #     for wav in wav_generator:
        #         array = wav.numpy()
        #         yield {
        #             'wav': array.tobytes(),
        #             'sample_width': array.dtype.itemsize,
        #             'frame_rate': array.shape[0],
        #             'channels': array.shape[1],
        #         }

        # logging.debug("Streaming audio to client...")

        # return StreamingResponse(stream_audio(), media_type="audio/wav")
        io_bytes = io.BytesIO()
        soundfile.write(io_bytes, wav, toneconverter.hps.data.sampling_rate, format='WAV', subtype='PCM_16')
        await websocket.send_bytes(io_bytes.getvalue())
        logging.debug("Completed websocket request at /api/v1/tts in %s seconds", inference_end)

if __name__ == '__main__':
    from say.entry_points import run_say
    run_say.run()
