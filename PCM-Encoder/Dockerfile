FROM alpine:3.19

WORKDIR /app

RUN apk add --no-cache ffmpeg

COPY audio/ audio/
COPY create_pcm.sh .

RUN chmod +x create_pcm.sh

CMD ["sh", "./create_pcm.sh"]

