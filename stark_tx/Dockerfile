FROM python:3.9

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./app/pyproject.toml ./app/poetry.lock* /app/

COPY ./app/start.sh  /start.sh
RUN chmod +x /start.sh

COPY ./app/start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY ./app/gunicorn_conf.py /gunicorn_conf.py


# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY ./app /app
ENV PYTHONPATH=/app
