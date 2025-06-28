FROM debian:bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libfftw3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .  

RUN gcc -o pr-generator pr-generator.c -lfftw3

CMD ["./pr-generator"]