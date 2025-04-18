FROM python:3.13-slim
WORKDIR /app

COPY src/projects/findxai/pyproject.toml ./
COPY src/projects/findxai/poetry.lock ./

RUN pip install poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-root

COPY src/projects/findxai ./

EXPOSE 8080
CMD ["python", "/app/main.py"]