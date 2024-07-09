# Gathering Game Service 1.0
This service keeps all the game objects updated within Gathering.

# Prerequisites
* docker

## Setup
### Docker
```bash
docker run --restart=on-failure ghcr.io/zhaho/gathering-game-service:main
```
### Docker Compose
```bash
---
version: "3"

services:
  game-service:
    image: ghcr.io/zhaho/gathering-game-service:main
    restart: on-failure
```
