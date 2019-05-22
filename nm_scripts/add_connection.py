"""
Add a connection to NetworkManager. You do this by sending a dict to
AddConnection. The dict below was generated with n-m dump on an existing
connection and then anonymised.


############################################
# manually (in base balena OS) add a connection to the my hidden home AP:
nmcli c add type wifi con-name spanky ifname wlan0 ssid spanky
nmcli con modify spanky wifi-sec.key-mgmt wpa-psk
nmcli con modify spanky wifi-sec.psk <passwd>
nmcli con up spanky
nmcli

# In our container, use NM to dump the connection (and clean it up):
# ./net-man-util.py dump spanky
{'802-11-wireless': {'mode': 'infrastructure',
                     'security': '802-11-wireless-security',
                     'ssid': 'spanky'},
 '802-11-wireless-security': {'key-mgmt': 'wpa-psk', 'psk': '<passwd>'},
 'connection': {'id': 'spanky',
                'type': '802-11-wireless',
                'uuid': str(uuid.uuid4())},
 'ipv4': {'method': 'auto'},
 'ipv6': {'method': 'auto'}
}

############################################
# manually (in base balena OS) add a connection to the open MIT AP:
nmcli c add type wifi con-name MIT ifname wlan0 ssid MIT
nmcli con up MIT
nmcli

# In our container, use NM to dump the connection (and clean it up):
#./net-man-util.py dump MIT
{'802-11-wireless': {'mode': 'infrastructure',
                     'ssid': 'MIT'},
 'connection': {'id': 'MIT',
                'type': '802-11-wireless',
                'uuid': str(uuid.uuid4())},
 'ipv4': {'method': 'auto'},
 'ipv6': {'method': 'auto'}
}
"""

import NetworkManager
import uuid

#debugrob: use this format to get on MIT SECURE
example_connection = {
     '802-11-wireless': {'mode': 'infrastructure',
                         'security': '802-11-wireless-security',
                         'ssid': 'n-m-example-connection'},
     '802-11-wireless-security': {'auth-alg': 'open', 'key-mgmt': 'wpa-eap'},
     '802-1x': {'eap': ['peap'],
                'identity': 'eap-identity-goes-here',
                'password': 'eap-password-goes-here',
                'phase2-auth': 'mschapv2'},
     'connection': {'id': 'nm-example-connection',
                    'type': '802-11-wireless',
                    'uuid': str(uuid.uuid4())},
     'ipv4': {'method': 'auto'},
     'ipv6': {'method': 'auto'}
}

example_MIT_open_connection = {
 '802-11-wireless': {'mode': 'infrastructure',
                     'ssid': 'MIT'},
 'connection': {'id': 'MIT',
                'type': '802-11-wireless',
                'uuid': str(uuid.uuid4())},
 'ipv4': {'method': 'auto'},
 'ipv6': {'method': 'auto'}
}

example_hidden_AP_connection = {
 '802-11-wireless': {'mode': 'infrastructure',
                     'security': '802-11-wireless-security',
                     'ssid': 'spanky'},
 '802-11-wireless-security': {'key-mgmt': 'wpa-psk', 'psk': '<passwd>'},
 'connection': {'id': 'spanky',
                'type': '802-11-wireless',
                'uuid': str(uuid.uuid4())},
 'ipv4': {'method': 'auto'},
 'ipv6': {'method': 'auto'}
}

conn = example_hidden_AP_connection
#conn = example_MIT_open_connection
ret = NetworkManager.Settings.AddConnection(conn)
print(f"Added connection={conn} ret={ret}")




