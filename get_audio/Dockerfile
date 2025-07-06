FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    pip install --no-cache-dir yt-dlp

WORKDIR /app

COPY download_playlist.sh /app/download_playlist.sh
RUN chmod +x /app/download_playlist.sh

CMD ["/bin/bash", "/app/get_audio.sh"]
