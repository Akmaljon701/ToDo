FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /ToDoApp

# Copy the current directory contents into the container
COPY . /ToDoApp/

# Install Poetry
RUN pip install --upgrade pip && pip install poetry

# Install the project dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Expose port 8000 to allow external connections
EXPOSE 8008

# Define the command to run the application (remove invalid `&&`)
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8008"]
