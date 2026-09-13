FROM rocq/rocq-prover:9.2

USER root

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --break-system-packages --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R rocq:rocq /app

USER rocq

CMD ["gunicorn", "main:app"]