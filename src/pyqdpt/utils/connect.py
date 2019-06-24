import os
import socket
import subprocess
import time


def start_usb_ethernet(key='CDC/ECM', dest=None):
    data = {
        'RNDIS': b"\x01\x00\x00\x01\x00\x00\x00\x01\x00\x04",
        'CDC/ECM': b"\x01\x00\x00\x01\x00\x00\x00\x01\x01\x04",
    }
    if dest:
        devices = [dest]
    else:
        devices = [i for i in os.listdir('/dev') if i.startswith('ttyACM')]
    return_code = dict()
    for dev in devices:
        dest = '/dev/{}'.format(dev)
        if os.path.exists(dest) and not os.path.isfile(dest):
            return_code[dev] = open(dest, 'wb').write(data[key])
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
        for mod in kern_module:
            if len(line.split()) >= 2 and mod == line.split()[1]:
                kern_log.append(line)
                continue
    iface = kern_log[0].split()[3][:-1]
    return iface


def main():
    start_usb_ethernet('CDC/ECM')
    ip = ''
    while not ip:
        ip = resolve()
        time.sleep(1)
    return ip


if __name__ == "__main__":
    print(main())
    print(get_iface())
