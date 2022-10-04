ARG VARIANT=3.9-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

ENV PYTHONUNBUFFERED 1

RUN sudo apt-get update && sudo apt-get install -y \
  coreutils

# [Optional] Allow the vscode user to pip install globally w/o sudo
ENV PIP_TARGET=/usr/local/pip-global
ENV PYTHONPATH=${PIP_TARGET}:${PYTHONPATH}
ENV PATH=${PIP_TARGET}/bin:${PATH}
RUN if ! cat /etc/group | grep -e "^pip-global:" > /dev/null 2>&1; then groupadd -r pip-global; fi \
    && usermod -a -G pip-global vscode \
    && umask 0002 && mkdir -p ${PIP_TARGET} \
    && chown :pip-global ${PIP_TARGET} \
    && ( [ ! -f "/etc/profile.d/00-restore-env.sh" ] || sed -i -e "s/export PATH=/export PATH=\/usr\/local\/pip-global:/" /etc/profile.d/00-restore-env.sh )

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
COPY app/requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

ENV GUNICORN_TARGET=/var/run/gunicorn
RUN if ! cat /etc/group | grep -e "^var-global:" > /dev/null 2>&1; then groupadd -r var-global; fi \
    && usermod -a -G var-global vscode \
    && umask 0002 && mkdir -p ${GUNICORN_TARGET} \
    && chown :var-global ${GUNICORN_TARGET}

ENV STATIC_TARGET=/var/www/static
ENV MEDIA_TARGET=/var/www/media
RUN umask 0002 && mkdir -p ${STATIC_TARGET} && umask 0002 && mkdir -p ${MEDIA_TARGET} \
    && chown :var-global ${STATIC_TARGET} && chown :var-global ${MEDIA_TARGET}

COPY ./app/portfolio_site /workspace/app/portfolio_site

COPY ./app/bootstrap.sh /workspace/app/
RUN chmod 777 /workspace/app/bootstrap.sh

CMD [ "/bin/bash", "-c", "/workspace/app/bootstrap.sh"]
