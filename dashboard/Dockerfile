FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Scapy and GCC (for ELF compilation)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc6-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY dashboard/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy challenge generators
COPY challenges/ /tmp/challenges/

# Copy dashboard application code
COPY dashboard/ .

# Create directories
RUN mkdir -p /app/data /app/static/challenges

# Generate challenge artifacts during build
# Stage 02: PCAP file
RUN OUTPUT_PATH=/app/static/challenges/telemetry.pcap python /tmp/challenges/stage02_pcap/generate_pcap.py

# Stage 05: Simulated memory dump
RUN OUTPUT_PATH=/app/static/challenges/drone_core.raw python /tmp/challenges/stage05_forensics/generate_dump.py

# Stage 06: Compile the reverse engineering binary
RUN gcc -o /app/static/challenges/doomsday.elf /tmp/challenges/stage06_reversing/doomsday.c

# Clean up build dependencies and temp files
RUN rm -rf /tmp/challenges && \
    apt-get purge -y gcc libc6-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -s /bin/bash argus && \
    chown -R argus:argus /app
USER argus

EXPOSE 9000

CMD ["python", "app.py"]
