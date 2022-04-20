# BUILDER
# First, the builder installs poetry's dependencies and poetry itself.
# It then installs all dependencies (thus, this step can be cached if dependencies didn't change).
# Afterward, it builds the cli itself (via poetry) and installs it (via pip).
FROM python:3.8.5-slim as builder

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential

# install poetry
ENV POETRY_VERSION "1.0.3"
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH "/root/.poetry/bin:${PATH}"

COPY . /build/
WORKDIR /build

# create separate venv
RUN python -m venv /opt/venv && \
  . /opt/venv/bin/activate && \
  pip install --no-cache-dir -U 'pip>20'

# install dependencies
RUN . /opt/venv/bin/activate && poetry install --no-dev --no-root --no-interaction

# install quick
RUN . /opt/venv/bin/activate && \
  poetry build -f wheel -n && \
  pip install --no-deps dist/*.whl && \
  rm -rf dist *.egg-info

# make sure we use the virtualenv
ENV PATH="/opt/venv/bin:$PATH"

# RUNNER
# The runner copies the created venv from builder and actiates it. With that, only the bare minimum is included.
FROM python:3.8.5-slim as runner

# copy everything from /opt
COPY --from=builder /opt/venv /opt/venv

# make sure we use the virtualenv
ENV PATH="/opt/venv/bin:$PATH"

# update permissions & change user to not run as root
WORKDIR /app
RUN chgrp -R 0 /app && chmod -R g=u /app
USER 1001

# change shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENTRYPOINT ["quick"]
CMD ["--help"]
