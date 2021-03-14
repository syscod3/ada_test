########################################################################################
#
# This build stage builds the sources
#
######################################################################################## 

# pull official base image
FROM python:3.7.1-alpine as builder

COPY /app /app
COPY /server.py /server.py
WORKDIR /app

# Install Python dependencies
# install dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
    libressl-dev libffi-dev gcc musl-dev python3-dev \
    &&pip install --upgrade pip --upgrade setuptools \
    && pip install -r requirements.txt  

# create an anonymous user to be used with the distroless build
# as defined below.
RUN sed -i -r "/^(root|nobody)/!d" /etc/passwd /etc/shadow /etc/group \
    && sed -i -r 's#^(.*):[^:]*$#\1:/sbin/nologin#' /etc/passwd
RUN mkdir /data && touch /data/app.db

########################################################################################
#
# This build stage creates a distroless image for production.
#
########################################################################################

# python 3.7
FROM gcr.io/distroless/python3-debian10

EXPOSE 8800

COPY --from=builder /app /app
COPY --from=builder /server.py /server.py
COPY --from=builder /usr/local/lib/python3.7/site-packages /usr/local/lib/python3.7/site-packages
COPY --from=builder /etc/passwd /etc/shadow /etc/group /etc/
COPY --from=builder --chown=nobody /data /data

USER nobody

ENV APP /app
ENV DATABASE_PATH=/data/app.db

ENV PYTHONPATH=/usr/local/lib/python3.7/site-packages
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV LC_ALL C.UTF-8

CMD ["/server.py"]