# Display all visible SSIDs
# When connected to an AP, that is all that will be in the list.
# When there is no active connection, this will show all visible APs.

import NetworkManager

for dev in NetworkManager.NetworkManager.GetDevices():
    if dev.DeviceType != NetworkManager.NM_DEVICE_TYPE_WIFI:
        continue
    for ap in dev.GetAccessPoints():
        print('%-30s %dMHz %d%%' % (ap.Ssid, ap.Frequency, ap.Strength))


