# start / stop the dnsmasq process

import subprocess, time

DEFAULT_GATEWAY="192.168.42.1"
DEFAULT_DHCP_RANGE="192.168.42.2,192.168.42.254"
DEFAULT_INTERFACE="wlan0" # use 'ip link show' to see list of interfaces
saved_proc = None


def stop():
    if saved_proc is None:
        return
    saved_proc.terminate()
    saved_proc.kill()
    saved_proc = None
    print(f'stopped PID={saved_proc.pid}')


def start():
    path = "/usr/sbin/dnsmasq"
    args = [path]
    args.append("--address=/#/{DEFAULT_GATEWAY}")
    args.append("--dhcp-range={DEFAULT_DHCP_RANGE}")
    args.append("--dhcp-option=option:router,{DEFAULT_GATEWAY}")
    args.append("--interface={DEFAULT_INTERFACE}")
    args.append("--keep-in-foreground")
    args.append("--bind-interfaces")
    args.append("--except-interface=lo")
    args.append("--conf-file")
    args.append("--no-hosts" )

    # run dnsmasq in the background and save a reference to the object
    saved_proc = subprocess.Popen(args)

    # give a few seconds for the proc to start
    time.sleep(2)

    print(f'started {path}, PID={saved_proc.pid}')


