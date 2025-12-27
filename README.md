# QR Code Generator (Web UI)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/florianibach/qr-web)

[![DockerHub Repo](https://img.shields.io/badge/Docker_Hub-Repository-blue?logo=docker)](https://hub.docker.com/r/floibach/qr-web)

A lightweight, self-hosted QR code generator with a clean web interface.

---

This project is built and maintained in my free time.  
If it helps you or saves you some time, you can support my work on [![BuyMeACoffee](https://raw.githubusercontent.com/pachadotdev/buymeacoffee-badges/main/bmc-black.svg)](https://buymeacoffee.com/floibach)

Thank you for your support!


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


## Support me
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/floibach)

