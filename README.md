# AI Song Generator Core
End-to-End full song generator architecture including vocal synthesis, audio neural codecs, and hardware acceleration frameworks.

## Project Structure
- `pipeline_main.py`: Audio preprocessing pipeline (Demucs + G2P).
- `app_webui.py`: Gradio interface for browser-based song generation.
- `server_api.py`: FastAPI server for async audio streaming.
- `watermark.py`: Digital copyright management through audio watermarking.
- `triton_norm.py`: Hardware-accelerated normalization layers.
