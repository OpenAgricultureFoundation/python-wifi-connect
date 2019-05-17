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
