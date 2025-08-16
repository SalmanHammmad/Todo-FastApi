FROM python:3.11-slim
WORKDIR /code
RUN pip install --no-cache-dir poetry==1.8.2
COPY pyproject.toml /code/
RUN poetry install --no-root --no-interaction
COPY . /code
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
