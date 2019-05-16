#!/bin/bash

# Command line args:
#  -p <HTTP server port>       Default: 5000
#  -u <UI directory to serve>  Default: "../ui"
#  -h                          Show help.

python3.6 src/http_server.py $*
