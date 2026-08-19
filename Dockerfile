FROM python:3.11-slim
RUN pip install --no-cache-dir requests
COPY refresh_token.py /app/refresh_token.py
CMD ["python3", "/app/refresh_token.py"]
