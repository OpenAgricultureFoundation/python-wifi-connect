#!/usr/bin/env bash

echo "This script is optional."
echo "It verifies NetworkManager is installed."
echo "If not, installs it (and in the process disables the dhcpcd service)"
echo "Our OpenAg balena base OS already has NetworkManager and DBUS installed."
echo ""

check_os_version () {
    if [[ "$OSTYPE" != "linux"* ]]; then
        echo "ERROR: This application only runs on Linux."
        exit 1
    fi

    local _version=""
    if [ -f /etc/os-release ]; then
        _version=$(grep -oP 'VERSION="\K[^"]+' /etc/os-release)
    fi
    if [ "$_version" != "9 (stretch)" ]; then
        echo "ERROR: Distribution not based on Debian 9 (stretch)."
        exit 1
    fi
}

install_network_manager () {
    echo "Updating Debian package list..."
    apt-get update

    echo "Downloading NetworkManager..."
    apt-get install -y -d network-manager

    echo "Stopping dhcpcd..."
    systemctl stop dhcpcd
    systemctl disable dhcpcd
        
    echo "Installing NetworkManager..."
    apt-get install -y network-manager
    apt-get clean
}

# This only works on Linux
check_os_version

# Confirm the user wants to install...
read -r -p "Do you want to install? [y/N]: " response
response=${response,,}  # convert to lowercase
if [[ ! $response =~ ^(yes|y)$ ]]; then
    exit 0
fi

# Update packages and install
install_network_manager





