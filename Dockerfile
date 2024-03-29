# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-alpine AS build

RUN apk add build-base libffi-dev postgresql libpq-dev
RUN pip install poetry==1.5.1

WORKDIR /out

COPY poetry.lock pyproject.toml /out/
RUN poetry export --output requirements.txt --without-hashes

ADD manage.py /out/app/
ADD BFBC2_MasterServer /out/app/BFBC2_MasterServer
ADD Plasma /out/app/Plasma
ADD Theater /out/app/Theater
ADD easo /out/app/easo

RUN pip wheel -r requirements.txt -w wheels && cp requirements.txt app/requirements.txt

FROM python:3.10-alpine AS runtime

WORKDIR /app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apk add libpq

COPY --from=build /out/app /app
COPY --from=build /out/wheels /tmp/wheels

# Install pip requirements
RUN pip install --no-index --find-links=/tmp/wheels -r requirements.txt

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" bfbc2emu && chown -R bfbc2emu /app
USER bfbc2emu

HEALTHCHECK CMD ["python", "manage.py", "healthcheck"]

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "BFBC2_MasterServer.asgi:application", "--proxy-headers"]
