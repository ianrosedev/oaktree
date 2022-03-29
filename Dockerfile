# Pull base image
FROM python:3.10.2

# Set enviorment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy Project
COPY . /code/

# Expose Django port 8000
EXPOSE 8000

# Serve Django with Gunicorn on port 8000 (1 worker)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "config.wsgi:application"]