FROM python:3.12.13

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
COPY ./configs ./configs

WORKDIR /usr/src/app/src

EXPOSE 13000

ENTRYPOINT ["python", "main.py"]
CMD ["--config", "../configs/local.yaml"]

