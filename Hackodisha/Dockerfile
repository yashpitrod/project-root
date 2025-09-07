FROM python:3.10-slim

WORKDIR /app

# Install system deps if needed (uncomment if numpy/scipy compile needed)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

COPY Hackodisha/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir gunicorn

COPY Hackodisha/ ./

ENV PYTHONUNBUFFERED=1 \
    PORT=5000

EXPOSE 5000

# Serve Flask app object named "app" from app.py via gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]


