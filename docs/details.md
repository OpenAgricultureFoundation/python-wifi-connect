# Implementation details intended for developers.

## How it works
1. Use NetworkManager (NM, I'm referring to the python module that communicates over the DBUS API to the NetworkManager debian package) to see if there is an active wifi connection, if so we exit with nothing to do.
1. Start the [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq) utility to forward DNS, run a DHCP server and advertise us as a router.
1. Use NM to create a local access point.
1. Start our HTTP server, which will use JS to ask for `/networks` where we use NM to get a list the list of local Access Points (AP).  We also add a place holder to the list for the user to supply the name of a hidden AP.
1. When the user connects their machine to the AP we advertise, we act as a captured portal and display our UI (in the `ui/` dir) which is a form that allows the user to pick a local wifi and supply a password.
1. The HTTP server process the form POST and uses NM to stop our AP and connect to the AP the user has selected.  If this fails we go back to step 2.
1. If the device is successfully connected to an AP, we stop dnsmasq and exit.


## Installation
- You must run `scripts/install.sh` one time to verify your OS and our requirements (python3.6) before running this application.

- See `scripts/optional_install_NetworkManager_on_Linux.sh` to install the debian package if you are doing your own thing.  It is 'optional' for us (OpenAg) because we already have it in our docker container image.

- Note: DBUS and NetworkManager (the python module and Linux package) only work on Linux.  I have developed this application on OSX, so there is a simulation mode that will supply a fake list of APs, mainly for UI development.  Under OSX you can't control any wifi settings.


## References
- This application uses the [python-networkmanager module](https://pypi.org/project/python-networkmanager/). 
- Source for the [python-networkmanager module](https://github.com/seveas/python-networkmanager) on GitHub.
- Documentation for the [python-networkmanager module](https://pythonhosted.org/python-networkmanager/).
- The above python module is just an API that communicates over DBUS to the [debian NetworkManager package](https://wiki.debian.org/NetworkManager) which must be installed.
- [DBUS NetworkManager API](https://developer.gnome.org/NetworkManager/1.2/spec.html)


## Py NetworkManager
See the `nm_scripts/` directory for the scripts I copied/modified to figure out how to use NM.  Once tested / grokked, this code will become part of the server that handles the user input.


## Why?
I ([Rob Baynes](https://github.com/rbaynes)) had to have a way to get a headless embedded Linux device connected to a local WiFi in as smooth and easy a manner as possible.  So anyone could make the connection, middle school students, teachers, my Mom...

Since we are using the [Balena cloud](https://www.balena.io/cloud) to deploy our food computer embedded application to our devices, it was logical to use the [wifi-connect](https://github.com/balena-io/wifi-connect) project they wrote.

The problem is that I needed to make some changes (to support hidden SSIDs) and progress on the open source project is slow.  I forked the project into our organizaion and started modifying it.  Also learning the Rust language at the same time.  I got stuck and gave up when the rustc compiler kept repeatedly crashing my Raspberry Pi Zero while building wifi-connect.  Attempt two was to cross compile wifi-connect on a Linux x86-64 macine built for ARMv6 and ARMv7.  Neither worked and both core dumped.  So at this point, after wasting 3 days, I decided to rewite the application using Python3.6 (which is the same language we use for all our OpenAg projects).

I hope you enjoy and add to / extend this project!
[-rob](https://github.com/rbaynes)
