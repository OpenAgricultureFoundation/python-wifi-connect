# Display all visible SSIDs
# When connected to an AP, that is all that will be in the list.
# When there is no active connection, this will show all visible APs.

import NetworkManager

NM_SECURITY_NONE       = 0x0
NM_SECURITY_WEP        = 0x1
NM_SECURITY_WPA        = 0x2
NM_SECURITY_WPA2       = 0x4
NM_SECURITY_ENTERPRISE = 0x8

USER_INPUT_NONE     = 0x0
USER_INPUT_PASSWORD = 0x1
USER_INPUT_USERNAME = 0x2

for dev in NetworkManager.NetworkManager.GetDevices():
    if dev.DeviceType != NetworkManager.NM_DEVICE_TYPE_WIFI:
        continue
    for ap in dev.GetAccessPoints():
        #print('%-30s %dMHz %d%%' % (ap.Ssid, ap.Frequency, ap.Strength))

        # Get Flags, WpaFlags and RsnFlags, both are bit OR'd combinations of the
        # NM_802_11_AP_SEC_* bit flags.
        # https://developer.gnome.org/NetworkManager/1.2/nm-dbus-types.html#NM80211ApSecurityFlags

        security = NM_SECURITY_NONE
        user_input = USER_INPUT_NONE

        if ap.Flags & NetworkManager.NM_802_11_AP_FLAGS_PRIVACY and \
                ap.WpaFlags == NetworkManager.NM_802_11_AP_SEC_NONE and \
                ap.RsnFlags == NetworkManager.NM_802_11_AP_SEC_NONE:
            security = NM_SECURITY_WEP
            user_input = USER_INPUT_PASSWORD

        if ap.WpaFlags != NetworkManager.NM_802_11_AP_SEC_NONE:
            security = NM_SECURITY_WPA
            user_input = USER_INPUT_PASSWORD

        if ap.RsnFlags != NetworkManager.NM_802_11_AP_SEC_NONE:
            security = NM_SECURITY_WPA2
            user_input = USER_INPUT_PASSWORD

        if ap.WpaFlags & NetworkManager.NM_802_11_AP_SEC_KEY_MGMT_802_1X or \
                ap.RsnFlags & NetworkManager.NM_802_11_AP_SEC_KEY_MGMT_802_1X:
            security = NM_SECURITY_ENTERPRISE
            user_input = USER_INPUT_PASSWORD
            user_input |= USER_INPUT_USERNAME

        security_str = ''
        if security == NM_SECURITY_NONE:
            security_str = 'NONE'

        if security & NM_SECURITY_WEP:
            security_str += 'WEP '

        if security & NM_SECURITY_WPA:
            security_str += 'WPA '

        if security & NM_SECURITY_WPA2:
            security_str += 'WPA2 '

        if security & NM_SECURITY_ENTERPRISE:
            security_str += 'ENTERPRISE'

        input_str = ''
        if user_input == USER_INPUT_NONE:
            input_str = 'NONE'

        if user_input & USER_INPUT_USERNAME:
            input_str += 'USERNAME '

        if user_input & USER_INPUT_PASSWORD:
            input_str += 'PASSWORD '

        print(f'{ap.Ssid:15} Flags=0x{ap.Flags:X} WpaFlags=0x{ap.WpaFlags:X} RsnFlags=0x{ap.RsnFlags:X} Security={security_str:10} Input={input_str}')




