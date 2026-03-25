# ── Stage 1: Build Vue frontend ──────────────────────────────────
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile
COPY frontend/ ./
RUN pnpm build

# ── Stage 2: Django backend + serve static frontend ──────────────
FROM python:3.11-slim
LABEL maintainer="xjt-campus-laf"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=backend.settings

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project
COPY . .

# Copy built Vue frontend to Django static dir
COPY --from=frontend-builder /app/frontend/dist /app/frontend_dist

# Collect static files
RUN mkdir -p /app/staticfiles /app/media && \
    python manage.py collectstatic --noinput 2>/dev/null || true

# Copy nginx config
COPY deploy/nginx.conf /etc/nginx/sites-available/default
RUN ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default && \
    rm -f /etc/nginx/sites-enabled/default.bak 2>/dev/null || true

# Copy supervisor config
COPY deploy/supervisord.conf /etc/supervisor/conf.d/app.conf

EXPOSE 80

# Copy and set entrypoint
COPY deploy/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
