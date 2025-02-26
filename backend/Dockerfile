FROM python:3.12

WORKDIR /app

# Install Poetry to manage dependencies
RUN pip install poetry

# Configure Poetry to install dependencies into the system Python, not a virtual environment
ENV POETRY_VIRTUALENVS_CREATE=false

# Copy only the Poetry configuration files first to leverage Docker caching
COPY pyproject.toml poetry.lock ./

# Install dependencies directly from Poetry without installing the project itself
RUN poetry install --no-root

# Copy the rest of the application code
COPY . .

# Run the FastAPI application with Gunicorn and Uvicorn workers
CMD ["uvicorn", "main:app", "--port", "8080", "--host", "0.0.0.0"]
