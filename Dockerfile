# syntax=docker/dockerfile:1
# Keep this syntax directive! It's used to enable Docker BuildKit

# source: https://gist.github.com/usr-ein/c42d98abca3cb4632ab0c2c6aff8c88a
# Based on https://github.com/python-poetry/poetry/discussions/1879?sort=top#discussioncomment-216865
# but I try to keep it updated (see history)

################################
# poetry-base
# Sets up all our shared environment variables
################################
FROM python:3.11 as poetry-base

    # python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.7.1 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" 


# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential \
        # deps for ColBERT
        git

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
# The --mount will mount the buildx cache directory to where 
# Poetry and Pip store their cache so that they can re-use it
RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python3 -

# copy app files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY . ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-root 

#  --> also download required ColBERT model files
RUN poetry run python docs_qa/preload_colbert.py

CMD ["poetry", "run", "python", "bolt.py"]
