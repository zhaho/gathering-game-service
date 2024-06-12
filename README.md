# Gathering Game Service
This service keeps all the game objects within Gathering updated with game data.

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
