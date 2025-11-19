FROM python:3.12-slim

LABEL maintainer="somalet"
LABEL description="Originalny demo app with CI/CD pipeline"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
EXPOSE 8000

CMD ["python", "app.py"]
