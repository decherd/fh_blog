# The blog, as the server runs it. Posts and images are part of the image, so a
# new post is a rebuild and the container keeps no state of its own.
FROM python:3.12-slim@sha256:cb33f7f771ecec2ef1225cf39b159591a040391bd73e4c01f00fdfc4c47611d2

# Debian security fixes newer than the pinned base image. The weekly rebuild
# on the server (server/systemd/container-refresh) skips the build cache, so
# this runs again each week.
RUN apt-get update && apt-get -y upgrade && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dependencies first, so editing a post does not reinstall them.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt uvicorn

COPY . .

# Nothing here needs root.
RUN useradd --create-home blog && chown -R blog:blog /app
USER blog

EXPOSE 5001

# serve() only runs when main.py is the program being run, so importing it here
# gives the app without starting a second server. Live reload stays off: it is
# for writing posts locally, not for the site people read.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]
