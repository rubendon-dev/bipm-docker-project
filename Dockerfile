FROM python:3.12-slim-bookworm
WORKDIR /app
COPY app/requirements.txt .
RUN pip install -r requirements.txt
COPY app/ .
EXPOSE 80
CMD ["python", "app.py"]