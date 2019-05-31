# Implementation details intended for developers.

When I refer to 'NetworkManager' as 'NM', I'm referring to the python module that communicates over the DBUS API to the NetworkManager Linux service.


## How the application works
1. Check if there is an active internet connection, if so we exit with nothing to do.
1. Start the [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq) utility to forward DNS, run a DHCP server and advertise us as a new wifi router.
1. Get and save a list of available Access Points (AP) and add a special place holder so the user can provide a hidden AP.
1. Use NM to create a local 'hotspot' AP.
1. Start our HTTP server.
1. When the user connects their machine to the AP we advertise, we act as a captured portal and display our user interface (UI) (in the `ui/` dir) which is an HTML form that allows the user to pick a local wifi and supply a password.
1. When a browser loads the UI, a bit of [javascript](../ui/js/index.js) is run which requests `/networks` from the HTTP server, a REST request.  The server returns the list of AP we collected in step 3.
1. The HTTP server processes the form POST and uses NM to stop our hotspot and connect to the AP the user has selected.  If this fails we go back to step 3.
1. If the device is successfully connected to an AP, we stop dnsmasq and exit.

[See this flow diagram (lifted from balena)](images/flow.png) to visually show what is going on.


## References
- This application uses the [python-networkmanager module](https://pypi.org/project/python-networkmanager/). 
- Source for the [python-networkmanager module](https://github.com/seveas/python-networkmanager) on GitHub.
- Documentation for the [python-networkmanager module](https://pythonhosted.org/python-networkmanager/).
- The above python module is just an API that communicates over DBUS to the [debian NetworkManager package](https://wiki.debian.org/NetworkManager) which must be installed.
- [DBUS NetworkManager API](https://developer.gnome.org/NetworkManager/1.2/spec.html)
- [The Rust language version of this application written by balena.io](https://github.com/balena-io/wifi-connect) is a great reference!


## Py NetworkManager
See the `nm_scripts/` directory for the scripts I copied/modified to figure out how to use NM.  Once tested / grokked, this code was integrated into the python HTTP server which handles user input.

## Development setup
I [use this serial console cable](console_cable.md) setup to do development on the Raspberry Pi.


## Why?
I ([Rob Baynes](https://github.com/rbaynes)) had to have a way to get a headless embedded Linux device connected to a local WiFi in as smooth and easy a manner as possible.  So anyone could make the connection, middle school students, teachers, my Mom...

Since we are using the [Balena cloud](https://www.balena.io/cloud) to deploy our food computer embedded application to our devices, it was logical to use the [wifi-connect](https://github.com/balena-io/wifi-connect) project they wrote.

The problem is that I needed to make some changes (to support hidden SSIDs) and progress on the open source project is slow.  I forked the project into our organizaion and started modifying it.  Also learning the Rust language at the same time.  I got stuck and gave up when the rustc compiler kept repeatedly crashing my Raspberry Pi Zero while building wifi-connect.  Attempt two was to cross compile wifi-connect for ARMv6 and ARMv7 on a Linux x86-64 machine.  Neither worked and both binaries core dumped when run on the RPi.  So at this point, after wasting 3 days, I decided to rewite the application using Python3.6 (which is the same language we use for all our OpenAg projects).

I hope you enjoy and add to this project!
[-rob](https://github.com/rbaynes)

