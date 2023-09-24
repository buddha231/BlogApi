# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables for Django
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=blog.settings

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copy the current directory contents into the container at /app

COPY . /app

EXPOSE 8000

CMD ["gunicorn", "blog.wsgi:application", "--bind", "0.0.0.0:8000"]
