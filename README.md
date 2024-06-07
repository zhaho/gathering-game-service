# Gathering Game Service
This service keeps all the games updated with data.

## Installation
* Setup .env file.
* Create docker-compose.yml file
```yaml
---
version: "3"

services:
  game:
    image: ghcr.io/zhaho/gathering-game-service:main
    build: ./gathering-game-service
    restart: always
    command: python main.py
```
