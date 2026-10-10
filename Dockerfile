FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends     git curl ffmpeg libsndfile1 build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir torch torchaudio
EXPOSE 7860
CMD ["python", "app_webui.py"]
