# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install uv and build dependencies
RUN pip install uv setuptools wheel

# Copy project files
COPY pyproject.toml README.md ./
COPY users/ users/
COPY messages/ messages/
COPY main.py db.py ./

# Create virtual environment and install dependencies using uv
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install -e .

# Create a script to run the application with nohup
RUN echo '#!/bin/bash\nsource .venv/bin/activate\nnohup uvicorn main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &' > /app/start.sh
RUN chmod +x /app/start.sh

# Expose port 8000
EXPOSE 8000

# Set the entrypoint to the start script
ENTRYPOINT ["/app/start.sh"] 