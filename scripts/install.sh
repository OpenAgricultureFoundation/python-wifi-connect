#!/usr/bin/env bash

# Check OS we are running on.  NetworkManager only works on Linux.
if [[ "$OSTYPE" != "linux"* ]]; then
    echo "ERROR: This application only runs on Linux."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "WARNING: OSX is only supported for development/simulation."
        echo "NetworkManager and DBUS won't install or work on OSX."
    else
        exit 1
    fi
fi

# Save the path to THIS script (before we go changing dirs)
TOPDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# The top of our source tree is the parent of this scripts dir
TOPDIR+=/..
cd $TOPDIR

# Check if python3 and pip are installed
echo "Checking that python3 and pip are installed..."
INSTALL_PATH=`which python3`
if [[ ! -f "$INSTALL_PATH" ]]; then
    echo "ERROR: python3 is not installed."
    exit 1
fi
INSTALL_PATH=`which pip3`
if [[ ! -f "$INSTALL_PATH" ]]; then
    echo "ERROR: pip3 is not installed."
    exit 1
fi

# Remove any existing virtual environment
rm -fr $TOPDIR/venv

# Create a virtual environment (venv)
echo "Creating a python virtual environment..."
python3 -m venv $TOPDIR/venv

# Only install python modules on Linux (they are OS specific).
if [[ "$OSTYPE" == "linux"* ]]; then
    # Use the venv
    source $TOPDIR/venv/bin/activate

    # Install the python modules our app uses into our venv
    echo "Installing python modules..."
    pip3 install -r $TOPDIR/config/requirements.txt

    # Deactivate the venv
    deactivate
fi

echo "Done."

