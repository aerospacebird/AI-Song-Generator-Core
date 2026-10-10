import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Music Generation Engine API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def audio_stream_generator(lyrics: str, genre: str):
    for chunk_idx in range(1, 21):
        await asyncio.sleep(0.5)
        pseudo_audio_bytes = b"\x00\x01" * 32768
        yield pseudo_audio_bytes

@app.get("/api/v2/generate-stream")
async def get_audio_stream(lyrics: str = "가을 낙엽아", genre: str = "K-Pop Ballad"):
    return StreamingResponse(audio_stream_generator(lyrics, genre), media_type="audio/wav")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
