# ---- Base image -------------------------------------------------
FROM python:3.11-slim

# ---- System packages --------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
        git wget libglib2.0-0 libsm6 libxext6 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# ---- Non-root user ----------------------------------------------
ARG UID=1000
ARG GID=1000
RUN groupadd -g ${GID} appuser && \
    useradd -m -u ${UID} -g ${GID} -s /bin/bash appuser

WORKDIR /home/appuser/work
USER appuser

# ---- Copy project -----------------------------------------------
COPY --chown=appuser:appuser . /home/appuser/work

# ---- Install dependencies ---------------------------------------
RUN python -m venv /home/appuser/venv && \
    . /home/appuser/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

ENTRYPOINT ["/home/appuser/venv/bin/python", "-m", "app.main"]
CMD []
