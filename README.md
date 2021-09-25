# AmazonCrawler

Scrape Today's Deal page using requests_html python

## Setup

```sh
  pip install  -r requirements.txt
```

## Host api in Local for (dev)

```
uvicorn server:app --reload
```

localhost:8000

## Deployement

```
uvicorn main:app --host 0.0.0.0 --port 80
```
