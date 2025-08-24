FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Clean up requirements.txt to remove duplicates and conflicts that cause early build failures
RUN cat requirements.txt | sort | uniq > requirements_sorted.txt && \
    grep -v "^aiohttp$" requirements_sorted.txt | \
    grep -v "^openai$" | \
    grep -v "^Flask-CORS$" | \
    grep -v "^trafilature$" | \
    sed 's/tradingview_ta/tradingview-ta/g' > requirements_clean.txt && \
    echo "Successfully cleaned requirements - removed duplicates and conflicts" && \
    head -10 requirements_clean.txt

# Install Python dependencies from cleaned requirements
RUN python -m pip install -r requirements_clean.txt --no-cache-dir

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Expose port
EXPOSE 5000

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=5000
ENV FLASK_ENV=production

# Add health check directly in Docker - install curl first
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["python", "app.py"]