# Gathering Game Service
This service keeps all the games updated with gamedata.

## Installation.
* Set environment variables in docker-compose.yml file
```yaml
---
---
version: "3"

services:
  game_data:
    image: ghcr.io/zhaho/gathering-game-service:main
    restart: on-failure
    build: .
    environment:
      - BGG_API_URL=
      - BGG_API_ENDPOINT_BOARDGAME=
      - GATHERING_API_URL=
      - GATHERING_API_URL_NODATA=
      - PRICE_LOOKUP_URL=
      - LOG_DESTINATION=
    command: python main.py

```
Then all you have to do is to run:
```
docker-compose up -d
```
