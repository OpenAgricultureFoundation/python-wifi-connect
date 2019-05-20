import NetworkManager

### Run this before we run 'wifi-connect' to clear out pre-configured networks
def clear_connections():
    # Get all known connections
    connections = NetworkManager.Settings.ListConnections()

    # Delete the '802-11-wireless' connections
    for connection in connections:
        if connection.GetSettings()["connection"]["type"] == "802-11-wireless":
            if connection.GetSettings()["connection"]["id"].startswith("resin-wifi"):
                continue # don't kill the balena internal wifi
            print(
                "BalenaNetworkUtility: Deleting connection "
                + connection.GetSettings()["connection"]["id"]
            )
            connection.Delete()

if __name__=="__main__":
    clear_connections()

"""
We don't want to kill the resin wifi I think.  

BalenaNetworkUtility: Deleting connection resin-wifi-01
BalenaNetworkUtility: Deleting connection spanky
"""
