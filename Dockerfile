# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi==0.109.0 \
    uvicorn[standard]==0.27.0 \
    httpx==0.26.0 \
    pydantic==2.5.3 \
    pydantic-settings==2.1.0 \
    python-dotenv==1.0.0

# Copy the zip file (you'll mount this volume)
COPY govee-lights-api.zip .

# Extract the application
RUN unzip govee-lights-api.zip -d . && \
    rm govee-lights-api.zip

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

# Change ownership of the app directory to the non-root user
RUN chown -R app:app /app
USER app

# Expose port 8000 for FastAPI
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Run the application with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]