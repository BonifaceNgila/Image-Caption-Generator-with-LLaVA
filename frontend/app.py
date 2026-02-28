import streamlit as st
import requests

st.title("Image Caption Generator (LLaVA)")

BACKEND_URL = "http://localhost:8000/caption/"

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if st.button("Generate Caption"):
        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
        }
        try:
            response = requests.post(BACKEND_URL, files=files, timeout=60)
            response.raise_for_status()
            caption = response.json().get("caption", "Error generating caption.")
            st.subheader("Caption:")
            st.write(caption)
        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to backend at http://localhost:8000. "
                "Start FastAPI with: python -m uvicorn backend.main:app --reload"
            )
        except requests.exceptions.RequestException as exc:
            st.error(f"Request failed: {exc}")