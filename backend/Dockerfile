FROM python:3.11.10-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ARG APP_HOME=/home/app
ARG USER=app
ENV PATH="${PATH}:${APP_HOME}.local/bin"

RUN pip install --no-cache-dir --upgrade pip

RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME


COPY ./pyproject.toml ./poetry.lock $APP_HOME
RUN pip install --no-cache-dir --upgrade poetry poetry-plugin-export
RUN poetry export --without-hashes --without-urls --output requirements.txt
RUN poetry export --without-hashes --without-urls --only dev --output requirements.dev.txt
RUN poetry export --without-hashes --without-urls --only test --output requirements.test.txt
RUN pip uninstall poetry -y

RUN pip install --no-cache-dir -r requirements.txt

COPY . $APP_HOME

FROM builder AS testing

RUN pip install --no-cache-dir -r requirements.test.txt

ENTRYPOINT ["pytest", "-x", "-s", "tests"]


FROM builder AS development

RUN pip install --no-cache-dir -r requirements.dev.txt

ENTRYPOINT ["sh", "/home/app/docker/entrypoint.dev.sh"]


FROM builder AS production

RUN adduser $USER
RUN chown -R $USER $APP_HOME

RUN chmod +x $APP_HOME/docker/entrypoint.prod.sh

USER $USER

ENTRYPOINT ["sh", "/home/app/docker/entrypoint.prod.sh"]
