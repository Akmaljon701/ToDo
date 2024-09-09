# Use the official Python image as a base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install --upgrade pip && pip install poetry

# Copy Poetry configuration files before the rest of the code to leverage Docker caching
COPY pyproject.toml poetry.lock /app/

# Install the project dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Copy the current directory contents into the container
COPY . /app/

# Run collectstatic command to gather static files
RUN python manage.py collectstatic --noinput

## Expose port 8000 to allow external connections
#EXPOSE 8008
#
## Define the command to run the application (remove invalid `&&`)
#CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
