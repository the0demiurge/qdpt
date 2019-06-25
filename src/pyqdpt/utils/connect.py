import os
import re
import socket
import subprocess
import time


def start_usb_ethernet(key='CDC/ECM', dev=None):
    data = {
        'RNDIS': b"\x01\x00\x00\x01\x00\x00\x00\x01\x00\x04",
        'CDC/ECM': b"\x01\x00\x00\x01\x00\x00\x00\x01\x01\x04",
    }
    if dev:
        devices = [dev]
    else:
        devices = ['/dev/{}'.format(dev) for dev in os.listdir('/dev') if dev.startswith('ttyACM')]
    return_code = dict()
    for dev in devices:
        if os.path.exists(dev) and not os.path.isfile(dev):
            return_code[dev] = open(dev, 'wb').write(data[key])
    return return_code


def resolve():
    try:
        ip = subprocess.check_output(['avahi-resolve', '-n', 'digitalpaper.local']).decode().split()
        if len(ip) > 1:
            ip = ip[1]
        return ip
    except socket.gaierror:
        return


def list_ifaces():
    os.listdir('/sys/class/net/')


def get_iface(kern_module=['cdc_ether', 'rndis_host']):
    data = subprocess.check_output('dmesg').decode().split('\n')
    kern_log = list()
    for line in data[::-1]:
        line = re.sub(r'\[[^\]]+\]\s*', '', line).split()
        for mod in kern_module:
            if len(line) > 0 and mod == line[0]:
                kern_log.append(line)
                continue
    iface = kern_log[0][2].rstrip(':')
    return iface


def main():
    dev = ''
    ip = ''
    iface = ''

    return_code = start_usb_ethernet('CDC/ECM')
    if len(return_code) > 0:
        dev = list(return_code)[0]
    for i in range(5):
        ip = resolve()
        time.sleep(1)
        try:
            iface = get_iface()
        except IndexError:
            pass
        if ip and iface:
            break
    return ip, iface, dev


if __name__ == "__main__":
    print(main())
