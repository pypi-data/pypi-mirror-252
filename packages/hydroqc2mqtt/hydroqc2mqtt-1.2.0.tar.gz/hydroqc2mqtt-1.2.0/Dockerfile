FROM registry.gitlab.com/hydroqc/hydroqc-base-container/3.11:latest@sha256:e6ef50dbb2f351fbd4e20c39512885bdcd62d202f05c8558a4d40ac2d9836763 as build-image

ARG HYDROQC2MQTT_VERSION

WORKDIR /usr/src/app

COPY setup.cfg pyproject.toml /usr/src/app/
COPY hydroqc2mqtt /usr/src/app/hydroqc2mqtt

# See https://github.com/pypa/setuptools/issues/3269
ENV DEB_PYTHON_INSTALL_LAYOUT=deb_system

ENV DISTRIBUTION_NAME=HYDROQC2MQTT
ENV SETUPTOOLS_SCM_PRETEND_VERSION_FOR_HYDROQC2MQTT=${HYDROQC2MQTT_VERSION}

RUN python3.11 -m venv /opt/venv

RUN --mount=type=tmpfs,target=/root/.cargo \
    curl https://sh.rustup.rs -sSf | \
    RUSTUP_INIT_SKIP_PATH_CHECK=yes sh -s -- -y && \
    export PATH="/root/.cargo/bin:${PATH}"

RUN if [ `dpkg --print-architecture` = "armhf" ]; then \
       printf "[global]\nextra-index-url=https://www.piwheels.org/simple\n" > /etc/pip.conf ; \
    fi

RUN --mount=type=tmpfs,target=/root/.cargo \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --upgrade setuptools_scm && \
    pip config set global.extra-index-url https://gitlab.com/api/v4/projects/32908244/packages/pypi/simple && \
    pip install --no-cache-dir .

RUN . /opt/venv/bin/activate && \
    pip install --no-cache-dir msgpack ujson


FROM python:3.11-slim-bookworm@sha256:110609b2b904da7fb1226a92b6c02af5d6d599c5993f6194d1366d0d6a8a8295
COPY --from=build-image /opt/venv /opt/venv
COPY --from=build-image /usr/src/app/hydroqc2mqtt /usr/src/app/hydroqc2mqtt
COPY --from=build-image /opt/venv/bin/hydroqc2mqtt /opt/venv/bin/hydroqc2mqtt

RUN \
    adduser hq2m \
        --uid 568 \
        --group \
        --system \
        --disabled-password \
        --no-create-home

USER hq2m

ENV PATH="/opt/venv/bin:$PATH"
ENV TZ="America/Toronto" \
    MQTT_DISCOVERY_DATA_TOPIC="homeassistant" \
    MQTT_DATA_ROOT_TOPIC="hydroqc" \
    SYNC_FREQUENCY=600

CMD [ "/opt/venv/bin/hydroqc2mqtt" ]
