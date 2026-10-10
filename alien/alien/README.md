# 🛸 Operation: Extraterrestrial Dawn

> A sequential cyber-investigation CTF platform simulating the tracking of 6 extraterrestrial factions on Earth.

![Classification](https://img.shields.io/badge/Classification-TOP%20SECRET-red)
![Stages](https://img.shields.io/badge/Stages-6-blue)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy%20→%20Hard-orange)

---

## 📋 Overview

**Operation: Extraterrestrial Dawn** is a fully themed Capture The Flag (CTF) platform featuring a sci-fi "Threat Assessment Dashboard" that serves as the scoreboard and narrative hub. Participants act as agents of A.R.G.U.S. (Alien Reconnaissance & Global Unified Security) tracking down six alien factions through progressive cybersecurity challenges.

### Challenge Domains

| Stage | Codename | Domain | Difficulty |
|-------|----------|--------|------------|
| 01 | The Landing Zone | OSINT / Reconnaissance | Easy |
| 02 | Intercepted Telemetry | Networking / Packet Analysis | Easy |
| 03 | Rosetta Stone | Cryptography | Moderate |
| 04 | The Syndicate Portal | Web Security (SQLi) | Moderate |
| 05 | The Crashed Core | Digital Forensics | Hard |
| 06 | The Mothership's Payload | Reverse Engineering | Hard |

---

## 🚀 Quick Start

### Prerequisites

- **Docker Engine** (20.10+)
- **Docker Compose** (v2.0+)
- **Host OS**: Kali Linux / Ubuntu 22.04 LTS (recommended)
- **Resources**: 2 vCPUs, 4GB RAM, 15GB Storage

### Deployment

```bash
# Clone the repository
cd alien

# Build and start all containers
docker-compose up -d --build

# Verify containers are running
docker-compose ps
```

### Access Points

| Service | URL | Description |
|---------|-----|-------------|
| A.R.G.U.S. Dashboard | http://localhost:9000 | Main CTF interface |
| Syndicate Portal | http://localhost:9001 | Stage 04 target |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Participant Machine                    │
│            (Kali Linux / Ubuntu 22.04 LTS)              │
└───────────────┬───────────────────┬─────────────────────┘
                │                   │
        Port 9000 │          Port 9001
                │                   │
┌───────────────┴───────────────────┴─────────────────────┐
│              Docker Network (172.25.0.0/16)              │
│                                                          │
│  ┌────────────────────┐    ┌─────────────────────────┐  │
│  │  A.R.G.U.S.        │    │  Syndicate Portal       │  │
│  │  Dashboard          │    │  (Stellar Dawn)         │  │
│  │  ─────────────      │    │  ─────────────────      │  │
│  │  Flask + SQLite     │    │  Flask + SQLite         │  │
│  │  Challenge Files    │    │  Vulnerable Login       │  │
│  │  Score Tracking     │    │  (SQL Injection)        │  │
│  └────────────────────┘    └─────────────────────────┘  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 🔧 Tools Required

Players should have the following tools available:

- **Web Browser** — For OSINT and web interaction
- **Wireshark / tshark** — Network packet analysis
- **CyberChef / Python** — Cryptographic decoding
- **Burp Suite** — Web security testing
- **strings, grep** — Binary analysis utilities
- **Ghidra / GDB / IDA Free** — Reverse engineering

---

## 🏁 Flag Format

All flags follow the format: `ALIEN{...}`

---

## ⚙️ Management

```bash
# Stop all containers
docker-compose down

# Reset all data (clear scores and databases)
docker-compose down -v
docker-compose up -d --build

# View logs
docker-compose logs -f dashboard
docker-compose logs -f portal

# Rebuild a specific service
docker-compose build dashboard
docker-compose up -d dashboard
```

---

## 🔒 Security Controls

- All containers run as **non-root** users
- Bridge network **restricted** to localhost
- SQLite in the portal uses **read-only** mode for challenge data
- **Stateless** container resets via Docker

---

## 📊 Scoring

| Stage | Points | Hint Penalty |
|-------|--------|--------------|
| 01 — OSINT | 100 | -5 |
| 02 — Networking | 150 | -10 |
| 03 — Cryptography | 200 | -10 |
| 04 — Web Security | 250 | -10 |
| 05 — Forensics | 300 | -15 |
| 06 — Reverse Eng. | 350 | -15 |
| **Maximum** | **1350** | |

---

## 📝 License

This CTF platform is designed for educational purposes as part of a cybersecurity curriculum.
