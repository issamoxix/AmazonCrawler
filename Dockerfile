FROM python:3

COPY . .

RUN python -m  pip install  -r requirements.txt


CMD uvicorn server:app --host 0.0.0.0 --port 80
