FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create data directory
RUN mkdir -p /app/data

# Create non-root user
RUN useradd -m -s /bin/bash syndicate && \
    chown -R syndicate:syndicate /app
USER syndicate

EXPOSE 9001

CMD ["python", "app.py"]
