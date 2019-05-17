#!/usr/bin/env bash

# Command line args:
#  -p <HTTP server port>       Default: 5000
#  -u <UI directory to serve>  Default: "../ui"
#  -s                          Simulate NetworkManager.
#  -h                          Show help.

# Check OS we are running on.  NetworkManager only works on Linux.
SIMULATE=""
if [[ "$OSTYPE" != "linux"* ]]; then
    echo "ERROR: This application only runs on Linux."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "WARNING: OSX is only supported for development/simulation."
        SIMULATE="-s"
    else
        exit 1
    fi
fi

# Save the path to THIS script (before we go changing dirs)
TOPDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
# The top of our source tree is the parent of this scripts dir
cd $TOPDIR

# Use the venv
source $TOPDIR/venv/bin/activate

# Start our application
python3.6 $TOPDIR/src/http_server.py $SIMULATE -u $TOPDIR/ui/ $*
