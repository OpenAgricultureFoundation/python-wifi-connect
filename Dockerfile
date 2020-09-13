FROM python:3.8.5-slim AS compile-image

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc
RUN apt-get install -y --no-install-recommends libdbus-glib-1-dev libdbus-1-dev

WORKDIR /app

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY ./config/requirements.txt .
RUN pip install -r requirements.txt

# ------------------------------------------------------------------------------------
FROM python:3.8.5-slim AS build-image

ARG DEFAULT_INTERFACE
ENV DEFAULT_INTERFACE ${DEFAULT_INTERFACE:-"wlan0"}

ARG DISABLE_HOTSPOT
ENV DISABLE_HOTSPOT ${DISABLE_HOTSPOT:-0}

ARG DEFAULT_GATEWAY
ENV DEFAULT_GATEWAY ${DEFAULT_GATEWAY:-"192.168.42.1"}

ARG DEFAULT_DHCP_RANGE
ENV DEFAULT_DHCP_RANGE ${DEFAULT_DHCP_RANGE:-"192.168.42.2,192.168.42.254"}

ARG DBUS_SYSTEM_BUS_ADDRESS
ENV DBUS_SYSTEM_BUS_ADDRESS ${DBUS_SYSTEM_BUS_ADDRESS:-"unix:path=/var/run/dbus/system_bus_socket"}

COPY --from=compile-image /opt/venv /opt/venv

RUN apt-get update
RUN apt-get install -y --no-install-recommends dbus dnsmasq 
#procps

#COPY src/ ./app/src/
#COPY nm_scripts/ ./app/nm_scripts/
COPY scripts/ ./app/scripts/
#COPY ui/ ./app/ui/

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

CMD app/scripts/run.sh
