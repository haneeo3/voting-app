FROM python:3.12-alpine
WORKDIR /app
COPY requirement.txt .
RUN pip install -r requirement.txt
COPY app/ ./app/
COPY templates/ ./templates/
EXPOSE 5000
CMD ["python3", "app/app.py"]
