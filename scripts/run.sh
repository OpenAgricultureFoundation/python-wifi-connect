#!/usr/bin/env bash

# Command line args:
#  -p <HTTP server port>       Default: 5000
#  -u <UI directory to serve>  Default: "../ui"
#  -h                          Show help.

# Check OS we are running on.  NetworkManager only works on Linux.
if [[ "$OSTYPE" != "linux"* ]]; then
    echo "ERROR: This application only runs on Linux."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "WARN: OSX is only supported for development/simulation."
    else
        exit 1
    fi
fi

# Save the path to THIS script (before we go changing dirs)
TOPDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# The top of our source tree is the parent of this scripts dir
TOPDIR+=/..
cd $TOPDIR

# Use the venv
source $TOPDIR/venv/bin/activate

# Start our application
python3.6 $TOPDIR/src/http_server.py $*
