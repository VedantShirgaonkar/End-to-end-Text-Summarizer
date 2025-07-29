FROM python:3.8-slim-bullseye

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libxml2-dev \
        libxslt1-dev \
        zlib1g-dev \
        awscli && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --cache-dir /tmp/cache -r requirements.txt

# Copy app files
COPY . .

# ✅ Make /app discoverable by Python
ENV PYTHONPATH=/app/src

# Expose the Flask port (Azure expects port 80)
EXPOSE 80

# Run using gunicorn (for production)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "app:app"]