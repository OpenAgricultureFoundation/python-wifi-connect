FROM balenalib/raspberrypi3-ubuntu-python:3.6-bionic-build

ARG DEFAULT_INTERFACE
ENV DEFAULT_INTERFACE ${DEFAULT_INTERFACE:-"wlan0"}
ARG DISABLE_HOTSPOT
ENV DISABLE_HOTSPOT ${DISABLE_HOTSPOT:-0}
ARG DEFAULT_GATEWAY
ENV DEFAULT_GATEWAY ${DEFAULT_GATEWAY:-"192.168.42.1"}
ARG DEFAULT_DHCP_RANGE
ENV DEFAULT_DHCP_RANGE ${DEFAULT_DHCP_RANGE:-"192.168.42.2,192.168.42.254"}

WORKDIR /usr/src/app
# RUN [ "cross-build-start" ]
#RUN install_packages \
#  network-manager
  # \
  #python3-networkmanager

#COPY . .
RUN apt update
RUN apt install -y dnsmasq

#RUN chmod +x scripts/*
#RUN scripts/install.sh
# RUN [ "cross-build-end" ]

ENV DBUS_SYSTEM_BUS_ADDRESS=unix:path=/var/run/dbus/system_bus_socket

#CMD scripts/run.sh
CMD sleep 900000
