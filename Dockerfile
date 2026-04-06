# Employee Database Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 employee && chown -R employee:employee /app
USER employee

# Create volume for database persistence
VOLUME /app/data

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sqlite3; conn = sqlite3.connect('/app/data/employee.db'); conn.close()" || exit 1

# Run tests on build
RUN pytest test_employee_db.py -v

# Default command
CMD ["python", "app.py"]

# Expose port if you add a web interface later
# EXPOSE 8000