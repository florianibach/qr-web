# QR Code Generator (Web UI)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/florianibach/qr-web)

A lightweight, self-hosted QR code generator with a clean web interface.

## Features
- Generate QR codes from text or URLs
- Optional embedded logo/image (centered)
- Configurable size, border and error correction (ECC)
- Mobile-friendly UI
- Multi-architecture Docker image (amd64 & arm64)
- Works perfectly on Raspberry Pi

## Usage (Docker)
### docker run
```
docker run --rm -p 8088:8000 floibach/qr-web:latest
```

### docker compose 
```yaml
services:
  qr-web:
    image: floibach/qr-web:latest
    ports:
      - "8088:8000"
    restart: unless-stopped
```
then open:
```
http://localhost:8088
```
### Notes

- Default error correction level: Q (recommended)
- For larger logos, use Q or H ECC
- No data is stored – everything runs in-memory

