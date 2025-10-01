# Dockerfile
FROM python:3.11-slim

WORKDIR /app

ARG GIT_BRANCH=main

# Install git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Clone repo and checkout branch
RUN git clone https://github.com/manojkumartjpk/es-search.git . \
    && git checkout $GIT_BRANCH 

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

ENV APP_BRANCH=$GIT_BRANCH

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
