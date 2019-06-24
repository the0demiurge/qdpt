import os


cert, key, device_id = dpt.register()
owner = dpt.get_owner()
info = dpt.get_info()
serial = info['serial_number']


def save_key(cert, key, device_id, serial, owner, save_path='~/.config/qdpt'):
    save_path = os.path.expanduser(save_path)
    os.makedirs(os.path.join(save_path, 'devices', device_id), exist_ok=True)
    for name, value in (
        ('cert', cert),
        ('key', key),
        ('owner', owner),
        ('serial', serial),
    ):
        with open(os.path.join(save_path, 'devices', device_id, name), 'w') as f:
            f.write(value)


def load_keys(save_path='~/.config/qdpt/devices'):
    save_path = os.path.expanduser(save_path)
    key_paths = os.listdir(save_path)
    keys = dict()
    for device_id in key_paths:
        key_data = dict()
        for name in ('cert', 'key', 'owner', 'serial'):
            with open(os.path.join(save_path, device_id, name)) as f:
                value = '\n'.join(f.readlines())
            key_data[name] = value
        keys[device_id] = key_data
    return keys
