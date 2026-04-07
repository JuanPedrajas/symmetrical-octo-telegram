# ---- Base image ----
FROM python:3.12-slim

# Install system deps + Node (modern version)
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean

WORKDIR /app

# ---- Install Poetry ----
RUN pip install --no-cache-dir poetry

# ---- Copy only dependency files first (cache optimization) ----
COPY backend/pyproject.toml ./backend/

WORKDIR /app/backend
RUN poetry lock
RUN poetry install --no-root

# ---- Frontend deps ----
WORKDIR /app
COPY frontend/package.json ./frontend/

WORKDIR /app/frontend
RUN npm install

# ---- Copy full project ----
WORKDIR /app
COPY . .

# ---- Build frontend (better than dev server) ----
WORKDIR /app/frontend
RUN npm run build

# Optional: move build into backend static
RUN mkdir -p /app/backend/static && \
    cp -r dist/* /app/backend/static/

# ---- Expose backend only ----
EXPOSE 8000

# ---- Start script ----
COPY docker/start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

CMD ["start.sh"]
