FROM python:3.7-alpine
COPY ./r.txt .
RUN apk add gcc musl-dev linux-headers g++ postgresql-libs postgresql-dev
RUN pip install -r r.txt
RUN pip install psycopg2