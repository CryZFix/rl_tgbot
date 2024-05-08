FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt && rm requirements.txt

WORKDIR /app

ADD src /app/

CMD ["python", "bot.py"]