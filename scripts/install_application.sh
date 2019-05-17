#!/usr/bin/env bash

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

# Check if python and pip (3.6) is installed
INSTALL_PATH=`which python3.6`
if [[ ! -f "$INSTALL_PATH" ]]; then
    echo "ERROR: python3.6 is not installed."
    exit 1
fi
INSTALL_PATH=`which pip3.6`
if [[ ! -f "$INSTALL_PATH" ]]; then
    echo "ERROR: pip3.6 is not installed."
    exit 1
fi

# Remove any existing virtual environment
sudo rm -fr $TOPDIR/venv

# Create a virtual environment (venv)
python3.6 -m venv $TOPDIR/venv

# Use the venv
source $TOPDIR/venv/bin/activate

# Install the python modules our app uses into our venv
pip3.6 install -r $TOPDIR/config/requirements.txt

# Deactivate the venv
deactivate
