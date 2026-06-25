# ─────────────────────────────────────────────────────────────
# Nginx Dockerfile — Ubuntu Base
# Author  : Pratik Mehta | Accion Labs
# Purpose : Serve a static website using Nginx on Ubuntu
# ─────────────────────────────────────────────────────────────

# Stage 1 — Base image
FROM ubuntu:22.04

# Metadata labels
LABEL maintainer="Pratik Mehta <pratik.mehta@accionlabs.com>"
LABEL version="1.0"
LABEL description="Nginx web server on Ubuntu 22.04"

# ── Environment variables ──────────────────────────────────
ENV DEBIAN_FRONTEND=noninteractive
ENV NGINX_VERSION=1.22.0
ENV APP_DIR=/var/www/html
ENV LOG_DIR=/var/log/nginx

# ── Install Nginx ──────────────────────────────────────────
# Combine update + install + cleanup in a single RUN layer
# to avoid bloating the image with apt cache
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        nginx=1.22.0-1ubuntu3 \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# ── Create a non-root user to run nginx ───────────────────
RUN groupadd --system webuser && \
    useradd --system --gid webuser --no-create-home webuser

# ── Copy application files ─────────────────────────────────
# Copy custom Nginx configuration
COPY config/nginx.conf        /etc/nginx/nginx.conf

# Copy virtual host config
COPY config/default.conf      /etc/nginx/conf.d/default.conf

# Copy static website content
COPY html/index.html          ${APP_DIR}/index.html
COPY html/about.html          ${APP_DIR}/about.html
COPY html/404.html            ${APP_DIR}/404.html

# Copy assets folder (CSS, JS, images)
COPY html/assets/             ${APP_DIR}/assets/

# ── Set correct ownership ──────────────────────────────────
RUN chown -R webuser:webuser ${APP_DIR} && \
    chown -R webuser:webuser ${LOG_DIR}

# ── Expose port ────────────────────────────────────────────
# Documents the port — publish using -p 80:80 at runtime
EXPOSE 80

# ── Health check ───────────────────────────────────────────
# Docker will mark container unhealthy if Nginx stops responding
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# ── Run as non-root ────────────────────────────────────────
USER webuser

# ── Start Nginx in foreground ─────────────────────────────
# daemon off keeps Nginx in the foreground so Docker can track the process
CMD ["nginx", "-g", "daemon off;"]
