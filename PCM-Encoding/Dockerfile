FROM jrottenberg/ffmpeg:6-ubuntu-edge

WORKDIR /app

COPY . .

RUN chmod +x create_pcm.sh

CMD ["sh", "create_pcm.sh"]

