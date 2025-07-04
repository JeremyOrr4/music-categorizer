FROM alpine:3.19

WORKDIR /app

COPY clean_pvc.sh .

RUN chmod +x clean_pvc.sh

CMD ["sh", "./clean_pvc.sh"]
