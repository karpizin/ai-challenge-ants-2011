FROM python:3.11-slim

# Установка системных зависимостей и компиляторов
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    openjdk-17-jdk-headless \
    nodejs \
    npm \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем всё содержимое проекта
COPY . .

# Делаем скрипты исполняемыми
RUN chmod +x engine/*.py engine/*.sh

# Директория для логов и реплеев
RUN mkdir -p replays

# По умолчанию запускаем тестовый матч
CMD ["python3", "engine/playgame.py", "--map_file", "maps/maze/maze_p02_01.map", "python3 engine/dist/sample_bots/python/RandomBot.py", "python3 engine/dist/sample_bots/python/HunterBot.py"]
