FROM python:3.7.4

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT [ "waitress-serve" ]
CMD ["--call", "app:create_app"]