FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    pip install --no-cache-dir yt-dlp

WORKDIR /app

COPY get_audio.sh.sh /app/get_audio.sh.sh
RUN chmod +x /app/get_audio.sh.sh

CMD ["/bin/bash", "/app/get_audio.sh"]
