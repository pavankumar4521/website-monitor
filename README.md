# Website Monitoring & Auto-Recovery System

## Overview
This project is a Python-based website monitoring system that performs real-time health checks, detects failures, and automatically triggers recovery actions using Docker.

It simulates a self-healing system commonly used in production environments.

---

## Features
- Monitors multiple websites continuously
- Detects failures (non-200 responses, unreachable endpoints)
- Tracks response time and flags slow services
- Logs structured output to a file (`monitor_logs.txt`)
- Triggers automated recovery actions
- Docker-based service restart capability
- CLI-based configuration (interval, timeout, threshold)
- Graceful shutdown handling

---

## Tech Stack
- Python
- Requests library
- Docker
- CLI (argparse)
- File handling

---

## Setup

### 1. Install dependencies
```bash
pip install requests
```

### 2. Start test service (Docker)
```bash
docker run -d -p 5000:80 --name mywebsite nginx
```

### 3. Run the Monitor
```bash
python monitor.py --interval 5 --timeout 3 --threshold 1
```

### Example output
- 🚨 [UNREACHABLE] | 2026-04-08 06:31:58 | http://localhost:5000
- ⚙️ Attempting recovery for: http://localhost:5000
- 🔁 Recovery executed: docker start mywebsite

(next cycle)

- ✅ [OK] | 2026-04-08 06:32:10 | http://localhost:5000 | 200 | 0.02s


