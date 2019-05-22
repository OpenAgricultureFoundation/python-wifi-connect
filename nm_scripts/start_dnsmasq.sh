#!/bin/bash

INSTALL_PATH=`which dnsmasq`
if [[ ! -f "$INSTALL_PATH" ]]; then
    echo "ERROR: dnsmasq is not installed."
    exit 1
fi

DEFAULT_GATEWAY="192.168.42.1"
DEFAULT_DHCP_RANGE="192.168.42.2,192.168.42.254"
DEFAULT_INTERFACE="wlan0" # use 'ip link show' to see list of interfaces

# run dnsmasq in the background
CMD="dnsmasq"\
' --address=/#/'$DEFAULT_GATEWAY\
" --dhcp-range=$DEFAULT_DHCP_RANGE"\
" --dhcp-option=option:router,$DEFAULT_GATEWAY"\
" --interface=$DEFAULT_INTERFACE"\
" --keep-in-foreground"\
" --bind-interfaces"\
" --except-interface=lo"\
" --conf-file"\
" --no-hosts" 

echo "Running in background: $CMD"
`$CMD` &


