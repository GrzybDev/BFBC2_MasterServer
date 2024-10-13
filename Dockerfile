FROM python:3.12-alpine AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PATH="/app/.venv/bin:$PATH"

# Rebuild the source code only when needed
FROM base AS builder

RUN apk add build-base libffi-dev postgresql-dev
RUN pip install poetry==1.8.2

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

# Production image, copy all the files and run next
FROM base AS runner

RUN apk add libpq --no-cache

WORKDIR /app

RUN addgroup --system --gid 1001 bfbc2emu
RUN adduser --system --uid 1001 bfbc2emu

COPY --chown=bfbc2emu:bfbc2emu bfbc2_masterserver ./bfbc2_masterserver
COPY --from=builder --chown=bfbc2emu:bfbc2emu /app/.venv ./.venv
ADD static /app/static

USER bfbc2emu

EXPOSE 8000
ENV PORT 8000

ENTRYPOINT [ "fastapi" ]
CMD [ "run", "bfbc2_masterserver" ]
