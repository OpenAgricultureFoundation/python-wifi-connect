import NetworkManager

### Run this before we run 'wifi-connect' to clear out pre-configured networks
def clear_connections():
    # Get all known connections
    connections = NetworkManager.Settings.ListConnections()

    # Delete the '802-11-wireless' connections
    for connection in connections:
        if connection.GetSettings()["connection"]["type"] == "802-11-wireless":
            print(
                "BalenaNetworkUtility: Deleting connection "
                + connection.GetSettings()["connection"]["id"]
            )
            connection.Delete()

if __name__=="__main__":
    clear_connections()

"""
debugrob, we don't wan tto kill the resin wifi I think.  Modify above to only delete the "active" connection found by show_current_AP.py

BalenaNetworkUtility: Deleting connection resin-wifi-01
BalenaNetworkUtility: Deleting connection spanky
(venv) 26 raspbian ~/python-wifi-connect/tests > [109187.454844] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
[109187.479916] brcmfmac: power management disabled
"""
