# Stage 1: Builder
FROM python:3.11-slim AS builder
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install Python dependencies to /root/.local
RUN pip install --upgrade pip \
    && pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
ENV TZ=UTC
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y cron tzdata && rm -rf /var/lib/apt/lists/*

# Configure timezone
RUN ln -sf /usr/share/zoneinfo/UTC /etc/localtime

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Create volume mount points
RUN mkdir -p /data /cron
RUN chmod 755 /data /cron

# Copy cron job configuration
COPY cron/2fa-cron /etc/cron.d/2fa-cron
RUN chmod 0644 /etc/cron.d/2fa-cron
RUN crontab /etc/cron.d/2fa-cron

# Expose API port
EXPOSE 8080

# Start cron and API server
CMD cron && uvicorn app:app --host 0.0.0.0 --port 8080
