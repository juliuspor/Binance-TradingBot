FROM python:3.12-slim

# Set Docker environment marker for detection
ENV DOCKER_CONTAINER=true

# Install dependencies including Chromium
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    git \
    chromium \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Chrome
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    CHROME_BIN=/usr/bin/chromium \
    CHROME_PATH=/usr/lib/chromium/ \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    DISPLAY=:99

# Tell WebDriverManager not to download drivers
ENV WDM_LOG_LEVEL=0 \
    WDM_PRINT_FIRST_LINE=False \
    WDM_LOCAL=True

# Update PATH to include ChromeDriver
ENV PATH="${PATH}:/usr/lib/chromium/"

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create directory for storing processed posts
RUN mkdir -p /app/data

# Set volume for persistent data
VOLUME ["/app/data"]

# Run the bot
CMD ["python", "src/main.py"]