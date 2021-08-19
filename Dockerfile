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
COPY python-pip-docker-template /usr/src/app/python-pip-docker-template/
COPY *.md /usr/src/app/python-pip-docker-template/
COPY conf/uwsgi.ini /app/
COPY conf/nginx/ /etc/nginx/conf.d/

WORKDIR /usr/src/app/python-pip-docker-template/
RUN python setup.py install
CMD python python-pip-docker-template/app.py

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="python-pip-docker-template" \
      org.label-schema.description="Here is a simple Python Flask for receiving a recording from doe.dialbox.cloud." \
      org.label-schema.url="https://www.sapian.cloud" \
      org.label-schema.vcs-url="https://git.sapian.com.co/Sapian/python-pip-docker-template" \
      org.label-schema.maintainer="sebastian.rojo@sapian.com.co" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vendor1="Sapian" \
      org.label-schema.version=$VERSION \
      org.label-schema.vicidial-schema-version="1"