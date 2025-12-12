# Stage 1: Builder
FROM python:3.11-slim AS builder
WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
ENV TZ=UTC
WORKDIR /app

RUN apt-get update && apt-get install -y cron tzdata && rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/share/zoneinfo/UTC /etc/localtime

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Fix for cron not finding Python modules
ENV PYTHONPATH=/app

COPY . .

# 🚨 CRITICAL FIX: Copy the private key file so the app.py can find it!
# This resolves the HTTP 500 Decryption failed error caused by FileNotFoundError.
COPY student_private.pem .
# --------------------------------------------------------------------------

RUN mkdir -p /data /cron && chmod 755 /data /cron

COPY cron/2fa-cron /etc/cron.d/2fa-cron
# CRITICAL FIX: Use tr to strip the carriage return (\r) character 
# that causes crontab errors on Windows/CRLF environments.
RUN tr -d '\r' < /etc/cron.d/2fa-cron > /etc/cron.d/2fa-cron.tmp \
    && mv /etc/cron.d/2fa-cron.tmp /etc/cron.d/2fa-cron \
    && chmod 0644 /etc/cron.d/2fa-cron \
    && crontab /etc/cron.d/2fa-cron

EXPOSE 8080

CMD ["sh", "-c", "cron && uvicorn app:app --host 0.0.0.0 --port 8080"]