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
# >> delete this if below works.
hotspot = {
 '802-11-wireless': {'mode': 'ap',
                     'ssid': 'PFC_EDU-'+os.getenv('RESIN_DEVICE_NAME_AT_INIT')},
 'connection': {'id': 'hotspot',
                'interface-name': 'wlan0',
                'type': '802-11-wireless',
                'uuid': str(uuid.uuid4())},
 'ipv4': {'method': 'auto'},
 'ipv6': {'method': 'auto'}
}

#debugrob: rust wifi-connect starts hostspot on 192.168.42.1:80
#debugrob: run: cd /usr/src/app && ./wifi-connect -s debugrob
# ./net-man-util.py dump debugrob

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
import os


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
}

NetworkManager.Settings.AddConnection(hotspot)
print(f"Added connection: {hotspot}")


