# Installing python-wifi-connect

## Note: this application only runs on Linux.

1. git clone https://github.com/OpenAgInitiative/python-wifi-connect.git
1. cd python-wifi-connect
1. ./scripts/install.sh

## Running
1. To see help: `./scripts/run.sh -h`
1. To run and exit if there is an active connection: `./scripts/run.sh`
1. To run and delete any active connections first: `./scripts/run.sh -d`
1. Go look for the `PFC_EDU-<unique name>` hotspot on your machine, you may have to turn OFF your wifi and turn it back on (I do) to see it.  If you pick it, the portal will show up.
1. Select one of the available wifis, and fill in the required security fields and click 'Connect'.
1. The application will exit when it is successfully connected.
1. If the user types an incorrect password, the hotspot is recreated and they can connect to it again to retry.
