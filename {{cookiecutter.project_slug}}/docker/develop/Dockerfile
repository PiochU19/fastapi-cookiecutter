ARG PYTHON_VERSION={{cookiecutter.python_version}}

# define an alias
FROM python:${PYTHON_VERSION}-slim-bullseye

###########
# BUILDER #
###########

FROM python as build-stage

# install and upgrade dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

RUN pip install --upgrade pip

# copy requirements file
COPY ./requirements.txt .

# install wheels
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt


#######
# RUN #
#######

FROM python as run-stage

ARG WORKDIR=/usr/src

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# set working directory
WORKDIR ${WORKDIR}

# install dependepncies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# copy wheels from build stage
# and install them
COPY --from=build-stage /wheels /wheels/
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

# COPY app folder
COPY ./app ./app
COPY ./docker/local/entrypoint.sh .

RUN ["chmod", "+x", "/entrypoint.sh"]

ENTRYPOINT ["/entrypoint.sh"]
