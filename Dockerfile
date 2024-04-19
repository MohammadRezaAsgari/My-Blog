# Use an official Python runtime as a base image
FROM python:3.8-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

EXPOSE 8000
CMD ["python", "./MyBuildingManager/manage.py", "runserver", "0.0.0.0:8000"]