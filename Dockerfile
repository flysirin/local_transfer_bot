FROM python:3.10.11-alpine3.17

ENV PYTHONUNBUFFERED TRUE

RUN apk add --no-cache curl

RUN pip3 install --no-cache-dir aiogram==3.0.0b6
RUN pip3 install  --no-cache-dir environs==9.5.0
RUN pip3 install  --no-cache-dir SQLAlchemy==2.0.29

COPY ./ /app

WORKDIR /app


EXPOSE 8080

CMD ["python3", "main.py"]
