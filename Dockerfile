FROM python:3.11-slim

RUN apt update && apt install -y \
    libportaudio2 \
    libasound2-dev \
    alsa-utils \
    gcc \
    build-essential \
    && apt clean

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-u", "monitor.py"]
