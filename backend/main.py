from fastapi import FastAPI, UploadFile, File
from fastapi import HTTPException
import requests
import base64

app = FastAPI()

@app.post("/caption/")
async def caption_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llava",
                "prompt": "Describe this image in one sentence.",
                "images": [image_base64],
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as exc:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama at http://localhost:11434. Ensure Ollama is running."
        ) from exc
    except requests.exceptions.Timeout as exc:
        raise HTTPException(
            status_code=504,
            detail="Timed out while waiting for Ollama response."
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Ollama request failed: {exc}"
        ) from exc

    try:
        result = response.json()
    except ValueError as exc:
        raise HTTPException(status_code=502, detail="Invalid JSON returned by Ollama.") from exc

    caption = result.get("response")
    if not caption:
        raise HTTPException(status_code=502, detail="Ollama response missing 'response' field.")

    return {"caption": caption.strip()}