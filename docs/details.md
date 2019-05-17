# Implementation details intended for developers.

## Installation
- You must run `scripts/install.sh` one time to verify your OS and our requirements (python3.6) before running this application.

- See `scripts/optional_install_NetworkManager_on_Linux.sh` to install the debian package if you are doing your own thing.  It is 'optional' because we already have it in our docker container.


## Docs
- This application uses the [python-networkmanager module](https://pypi.org/project/python-networkmanager/). 
- Source for the [python-networkmanager module](https://github.com/seveas/python-networkmanager) on GitHub.
- Documentation for the [python-networkmanager module](https://pythonhosted.org/python-networkmanager/).
- The above python module is just an API that communicates over DBUS to the [debian NetworkManager package](https://wiki.debian.org/NetworkManager) which must be installed.
- [DBUS NetworkManager API](https://developer.gnome.org/NetworkManager/1.2/spec.html)


## Why?
I ([Rob Baynes](https://github.com/rbaynes)) had to have a way to get a headless embedded Linux device connected to a local WiFi in as smooth and easy a manner as possible.  So anyone could make the connection, middle school students, teachers, my Mom...

Since we are using the [Balena cloud](https://www.balena.io/cloud) to deploy our food computer embedded application to our devices, it was logical to use the [wifi-connect](https://github.com/balena-io/wifi-connect) project they wrote.

The problem is that I needed to make some changes (to support hidden SSIDs) and progress on the open source project is slow.  I forked the project into our organizaion and started modifying it.  Also learning the Rust language at the same time.  I got stuck and gave up when the rustc compiler kept repeatedly crashing my Raspberry Pi Zero while building wifi-connect.  Attempt two was to cross compile wifi-connect on a Linux x86-64 macine built for ARMv6 and ARMv7.  Neither worked and both core dumped.  So at this point, after wasting 3 days, I decided to rewite the application using Python3.6 (which is the same language we use for all our OpenAg projects).

I hope you enjoy and add to / extend this project!
[-rob](https://github.com/rbaynes)
