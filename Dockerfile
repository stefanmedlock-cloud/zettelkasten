FROM python:3.10-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY zettelkasten/ ./zettelkasten/
RUN pip install --no-cache-dir .
EXPOSE 8080 8000
ENTRYPOINT ["zettelkasten", "run-server", "--host", "0.0.0.0", "--port", "8080", "--web-port", "8000"]
