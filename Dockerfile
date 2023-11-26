FROM python:3.12-slim

RUN apt update
RUN apt install -y git  # This was necessary because of python-creditcard git dependency

COPY credcrud /app/credcrud
COPY poetry.lock /app
COPY pyproject.toml /app

WORKDIR /app

RUN pip install .

EXPOSE 8765

CMD ["uvicorn", "credcrud.main:app", "--host", "0.0.0.0", "--port", "8765"]
