# Image Caption Generator (LLaVA)

This project uses the LLaVA vision-language model via Ollama to generate descriptive
captions for uploaded images.

## Features
- Vision-language model (LLaVA)
- FastAPI backend
- Streamlit UI

## How to Run
1. Pull the model:
   ollama pull llava
2. Start backend:
   uvicorn backend.main:app --reload
3. Start frontend:
   streamlit run frontend/app.py
4. Upload an image and generate a caption