# Campus Lost & Found - Django + Vue3
# Using Alpine for faster builds
FROM python:3.11-alpine
LABEL maintainer="xjt-campus-laf"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=backend.settings

WORKDIR /app

# Install system dependencies
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk update && apk add --no-cache \
    nginx \
    supervisor \
    bash \
    jpeg-dev \
    zlib-dev \
    gcc \
    musl-dev \
    && rm -rf /var/cache/apk/*

# Install Python deps (using PyMySQL - no C extensions needed)
COPY requirements.txt ./
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# Copy Django project
COPY backend/ ./backend/
COPY users/ ./users/
COPY items/ ./items/
COPY matches/ ./matches/
COPY manage.py ./
COPY seed_data.py ./

# Copy pre-built Vue frontend dist
COPY frontend/dist /app/frontend_dist

# Create directories
RUN mkdir -p /app/staticfiles /app/media /var/log/supervisor /run/nginx /etc/supervisor.d

# Collect Django static files
RUN python manage.py collectstatic --noinput 2>/dev/null || true

# Copy nginx config
COPY deploy/nginx.conf /etc/nginx/http.d/default.conf

# Copy supervisor config
COPY deploy/supervisord.conf /etc/supervisor.d/app.ini

# Copy entrypoint
COPY deploy/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80

CMD ["/entrypoint.sh"]
