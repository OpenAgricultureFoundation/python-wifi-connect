# Activate a connection by name

"""
If you are in the base Balena OS, you have access to nmcli, the NetworkManager
command line interface.  This is how Rob reconnects to his hidden home wifi
that his balana cloud image is configured to use:

#!/bin/sh
nmcli c add type wifi con-name spanky ifname wlan0 ssid spanky
nmcli con modify spanky wifi-sec.key-mgmt wpa-psk
nmcli con modify spanky wifi-sec.psk 1sparty0
nmcli con up spanky
"""

import NetworkManager
import sys

# Find the connection
name = sys.argv[1]
connections = NetworkManager.Settings.ListConnections()
connections = dict([(x.GetSettings()['connection']['id'], x) for x in connections])
for c in connections:
    print(f'connection {c}')

conn = connections[name]
print(f'found {name} connection {conn}')

# Find a suitable device
ctype = conn.GetSettings()['connection']['type']
print(f'ctype {ctype}')
dtype = {
    '802-11-wireless': NetworkManager.NM_DEVICE_TYPE_WIFI,
}.get(ctype,ctype)
print(f'dtype {dtype}')
devices = NetworkManager.NetworkManager.GetDevices()

for dev in devices:
    print(f'dev.DeviceType={dev.DeviceType} dev.State={dev.State}')
#    if dev.DeviceType == dtype and dev.State == NetworkManager.NM_DEVICE_STATE_DISCONNECTED:
    if dev.DeviceType == dtype:
        break
    else:
        dev = None

if dev == None:
    print("No suitable and available %s device found" % ctype)
    sys.exit(1)

# And connect
NetworkManager.NetworkManager.ActivateConnection(conn, dev, "/")

