# ---- Base image -------------------------------------------------
FROM python:3.11-slim

# ---- System packages --------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
        git wget libglib2.0-0 libsm6 libxext6 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# ---- Create user and working directory --------------------------
RUN useradd -m appuser
WORKDIR /home/appuser/work

# ---- Install Poetry (as root, in one layer) --------------------
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false

# ---- Copy only the files Poetry needs for caching ---------------
COPY --chown=appuser:appuser pyproject.toml poetry.lock* ./

# ---- Install production deps only (no test group) ---------------
RUN poetry install --only main --no-root

# ---- Switch to non-root user ------------------------------------
USER appuser

# ---- Copy source code -------------------------------------------
COPY --chown=appuser:appuser src ./src

WORKDIR /home/appuser/work/src

# ---- Entrypoint and default command -----------------------------
ENTRYPOINT ["python", "-m", "app.main"]
CMD []