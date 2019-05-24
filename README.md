# python-wifi-connect
An application that displays a wifi configuration UI for embedded Linux devices.

Inspired by the [wifi-connect](https://github.com/balena-io/wifi-connect) project written by [balena.io](https://www.balena.io/).

# Install and Run

Please read the [INSTALL.md](INSTALL.md) then the [RUN.md](RUN.md) files.


# How it works
![How it works](./docs/images/how-it-works.png?raw=true)

WiFi Connect interacts with NetworkManager, which should be the active network manager on the device's host OS.

### 1. Advertise: Device Creates Access Point

WiFi Connect detects available WiFi networks and opens an access point with a captive portal. Connecting to this access point with a mobile phone or laptop allows new WiFi credentials to be configured.

### 2. Connect: User Connects Phone to Device Access Point

Connect to the opened access point on the device from your mobile phone or laptop. The access point SSID is, by default, `PFC_EDU-<name>` where "name" is something random like "shy-lake" or "green-frog". 

### 3. Portal: Phone Shows Captive Portal to User

After connecting to the access point from a mobile phone, it will detect the captive portal and open its web page. Opening any web page will redirect to the captive portal as well.

### 4. Credentials: User Enters Local WiFi Network Credentials on Phone

The captive portal provides the option to select a WiFi SSID from a list with detected WiFi networks and enter a passphrase for the desired network.

### 5. Connected!: Device Connects to Local WiFi Network

When the network credentials have been entered, WiFi Connect will disable the access point and try to connect to the network. If the connection fails, it will enable the access point for another attempt. If it succeeds, the configuration will be saved by NetworkManager.

***
[See this for the development details and background.](docs/details.md)


