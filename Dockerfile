# pull official base image
FROM python:3.9.6-alpine3.14

# set environment varibles
ENV IS_DOCKER_CONTAINER Yes
ENV LOG_LEVEL INFO

# set work directory
WORKDIR /usr/src/app/

#RUN apk --no-cache add --virtual bash mariadb-connector-c
RUN apk --no-cache add bash \
	curl  \
	git

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /usr/src/app/Pipfile
RUN pipenv install --skip-lock --system

# copy project
COPY slack-matrix-migration /usr/src/app/slack-matrix-migration/
COPY *.md /usr/src/app/slack-matrix-migration/
COPY entrypoint.sh /usr/src/app/entrypoint.sh

WORKDIR /usr/src/app/slack-matrix-migration/
RUN python setup.py install
CMD python slack-matrix-migration/migrate.py

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="slack-matrix-migration" \
      org.label-schema.description="Migrates Users, Channels and all the conversations from a Slack export to Matrix" \
      org.label-schema.url="https://www.sapian.cloud" \
      org.label-schema.vcs-url="https://github.com/sapianco/slack-matrix-migration" \
      org.label-schema.maintainer="sebastian.rojo@sapian.com.co" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vendor1="Sapian" \
      org.label-schema.version=$VERSION
