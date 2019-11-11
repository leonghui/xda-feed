FROM python:alpine

RUN apk update && apk upgrade && \
    apk add --no-cache tzdata

COPY . /app/
WORKDIR /app/
RUN pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["server.py"]
