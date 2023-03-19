FROM python:3.9-slim


RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
        chromium \
        chromium-driver \
        xvfb \
        libfontconfig1 \
        libnss3 \
        libgconf-2-4 \
        libxi6 \
        libgconf-2-4 \
        libxss1 \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*
# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY /crawler/. /app/

# Start the application
CMD ["python", "main.py"]