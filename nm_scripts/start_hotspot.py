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
{'802-11-wireless': {'mode': 'ap',
                     'ssid': 'PFC_EDU'},
 'connection': {'id': 'hotspot',
                'interface-name': 'wlan0',
                'type': '802-11-wireless',
                'uuid': str(uuid.uuid4())},
 'ipv4': {'method': 'auto'},
 'ipv6': {'method': 'auto'}
}
"""

import NetworkManager
import uuid

#debugrob: use this format to get on MIT SECURE
hotspot = {
 '802-11-wireless': {'mode': 'ap',
                     'ssid': 'PFC_EDU'},
 'connection': {'id': 'hotspot',
                'interface-name': 'wlan0',
                'type': '802-11-wireless',
                'uuid': str(uuid.uuid4())},
 'ipv4': {'method': 'auto'},
 'ipv6': {'method': 'auto'}
}

NetworkManager.Settings.AddConnection(hotspot)
print(f"Added connection: {hotspot}")


