FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    SIS_DATA_FILE=/data/students.json \
    SIS_LOG_FILE=/tmp/app.log

WORKDIR /app
COPY src ./src
COPY config ./config

# Run as a non-root user; /data is the mount point for persistent storage.
RUN useradd --create-home sis && mkdir /data && chown sis /data
USER sis
VOLUME /data

# The app is an interactive menu: start it with `docker run -it`.
ENTRYPOINT ["python", "src/main.py"]
