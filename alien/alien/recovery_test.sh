#!/bin/bash

echo "=== CTF Play Box Recovery Test ==="

echo "[*] Testing Single Stage Reset (argus-dashboard)..."
docker-compose restart argus-dashboard

echo "[*] Waiting for 5 seconds..."
sleep 5

echo "[*] Testing Full Environment Reset..."
docker-compose down
docker-compose up -d

echo "=== Recovery Test Completed ==="