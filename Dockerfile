FROM python:3.9-slim

# Accept build arguments
ARG BGG_API_URL
ARG BGG_API_ENDPOINT_BOARDGAME
ARG GATHERING_API_URL
ARG GATHERING_API_URL_NODATA
ARG PRICE_LOOKUP_URL
ARG LOG_DESTINATION

# Set environment variables in the container
ENV BGG_API_URL=$BGG_API_URL
ENV BGG_API_ENDPOINT_BOARDGAME=$BGG_API_ENDPOINT_BOARDGAME
ENV GATHERING_API_URL=$GATHERING_API_URL
ENV GATHERING_API_URL_NODATA=$GATHERING_API_URL_NODATA
ENV PRICE_LOOKUP_URL=$PRICE_LOOKUP_URL
ENV LOG_DESTINATION=$LOG_DESTINATION


WORKDIR /app

COPY ./requirements.txt ./
RUN pip install xmltodict
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]