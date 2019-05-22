"""
Start a local hotspot using NetworkManager.
You do this by sending a dict to AddConnection. 
The dict below was generated with n-m dump on an existing connection and then anonymised.

# manually (in base balena OS) add a local hotspot with NO password (open)
nmcli connection add type wifi ifname wlan0 con-name hotspot autoconnect yes ssid PFC_EDU mode ap
nmcli connection modify hotspot 802-11-wireless.mode ap ipv4.method shared 
nmcli connection up hotspot

# if you want a password on the hotspot, add this to the modify command:
# 802-11-wireless-security.key-mgmt wpa-psk 802-11-wireless-security.psk 'PASSWORD'

# In our container, use NM to dump the connection (and clean it up):
# ./net-man-util.py dump hotspot
#
# Also check what the rust wifi-connect does
# cd /usr/src/app && ./wifi-connect -s hotspot

hotspot = {
 '802-11-wireless': {'band': 'bg',
                     'mode': 'ap',
                     'ssid': 'PFC_EDU-'+os.getenv('RESIN_DEVICE_NAME_AT_INIT')},
 'connection': {'autoconnect': False,
                'id': 'PFC_EDU',
                'interface-name': 'wlan0',
                'type': '802-11-wireless',
                'uuid': '8416b3ac-32fe-4d90-8d3b-e16d017d0f18'},
 'ipv4': {'address-data': [{'address': '192.168.42.1', 'prefix': 24}],
          'addresses': [['192.168.42.1', 24, '0.0.0.0']],
          'method': 'manual'},
 'ipv6': {'method': 'auto'}
"""

import NetworkManager
import uuid
import os, sys


connection_ID = 'PFC_EDU'
hotspot = {
 '802-11-wireless': {'band': 'bg',
                     'mode': 'ap',
                     'ssid': 'PFC_EDU-'+os.getenv('RESIN_DEVICE_NAME_AT_INIT')},
 'connection': {'autoconnect': False,
                'id': connection_ID,
                'interface-name': 'wlan0',
                'type': '802-11-wireless',
                'uuid': str(uuid.uuid4())},
 'ipv4': {'address-data': [{'address': '192.168.42.1', 'prefix': 24}],
          'addresses': [['192.168.42.1', 24, '0.0.0.0']],
          'method': 'manual'},
 'ipv6': {'method': 'auto'}
}

NetworkManager.Settings.AddConnection(hotspot)
print(f"Added connection: {hotspot}")

# Now find this connection and its device
connections = NetworkManager.Settings.ListConnections()
connections = dict([(x.GetSettings()['connection']['id'], x) for x in connections])
conn = connections[connection_ID]

# Find a suitable device
ctype = conn.GetSettings()['connection']['type']
dtype = {'802-11-wireless': NetworkManager.NM_DEVICE_TYPE_WIFI}.get(ctype,ctype)
devices = NetworkManager.NetworkManager.GetDevices()

for dev in devices:
    #if dev.DeviceType == dtype and dev.State == NetworkManager.NM_DEVICE_STATE_DISCONNECTED:
    if dev.DeviceType == dtype:
        break
else:
    print("No suitable and available %s device found" % ctype)
    sys.exit(1)

# And connect
NetworkManager.NetworkManager.ActivateConnection(conn, dev, "/")
print(f"Activated connection={conn}, dev={dev}.")


