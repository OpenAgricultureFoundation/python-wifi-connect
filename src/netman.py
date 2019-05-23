# Start a local hotspot using NetworkManager.

# You must use https://developer.gnome.org/NetworkManager/1.2/spec.html
# to see the DBUS API that the python-NetworkManager module is communicating
# over (the module documentation is scant).

import NetworkManager
import uuid, os, sys, time


#------------------------------------------------------------------------------
# Should do this before listing any APs or starting the hotspot.
def delete_all_wifi_connections():
    # Get all known connections
    connections = NetworkManager.Settings.ListConnections()

    # Delete the '802-11-wireless' connections
    for connection in connections:
        if connection.GetSettings()["connection"]["type"] == "802-11-wireless":
            print("Deleting connection "
                + connection.GetSettings()["connection"]["id"]
            )
            connection.Delete()


#------------------------------------------------------------------------------
# Return a list of connections
def get_list_of_access_points():
    #debugrob: get code from nm_scripts/show_current_AP.py
    pass


#------------------------------------------------------------------------------
# Returns True if we are connected to the internet, False otherwise.
def have_active_internet_connection():
    #debugrob: write this
    pass


#------------------------------------------------------------------------------
# Start a local hotspot on the wifi interface.
# Returns True for success, False for error.
def start_hotspot():
    connection_ID = 'hotspot'
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
    print(f"Added connection: {connection_ID}")

    # Now find this connection and its device
    connections = NetworkManager.Settings.ListConnections()
    connections = dict([(x.GetSettings()['connection']['id'], x) for x in connections])
    conn = connections[connection_ID]

    # Find a suitable device
    ctype = conn.GetSettings()['connection']['type']
    dtype = {'802-11-wireless': NetworkManager.NM_DEVICE_TYPE_WIFI}.get(ctype,ctype)
    devices = NetworkManager.NetworkManager.GetDevices()

    for dev in devices:
        if dev.DeviceType == dtype:
            break
    else:
        print(f"No suitable and available {ctype} device found.")
        return False

    # And connect
    NetworkManager.NetworkManager.ActivateConnection(conn, dev, "/")
    print(f"Activated connection={connection_ID}.")

    # Wait for ADDRCONF(NETDEV_CHANGE): wlan0: link becomes ready
    print(f'Waiting for connection to become active...')
    loop_count = 0
    while dev.State != NetworkManager.NM_DEVICE_STATE_ACTIVATED:
        #print(f'dev.State={dev.State}')
        time.sleep(2)
        loop_count += 1
        if loop_count > 100:
            break

    if dev.State == NetworkManager.NM_DEVICE_STATE_ACTIVATED:
        return True
    return False


