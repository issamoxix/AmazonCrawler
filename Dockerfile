FROM python:3

COPY . .

RUN python -m pip install requests-html

CMD python test.py