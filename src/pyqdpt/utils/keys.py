from pyqdpt import config_path
import os
import shutil
import logging
logger = logging.getLogger(__file__)

# cert, key, device_id = dpt.register()
# owner = dpt.get_owner()
# info = dpt.get_info()
# serial = info['serial_number']
key_path = os.path.join(config_path, 'devices')


def save_key(cert, key, device_id, serial, owner, key_path=key_path):
    save_path = os.path.join(key_path, device_id)
    existed = os.path.exists(save_path)
    os.makedirs(save_path, exist_ok=True)
    for name, value in (
        ('cert', cert),
        ('key', key),
        ('owner', owner),
        ('serial', serial),
    ):
        with open(os.path.join(key_path, device_id, name), 'w') as f:
            f.write(value)
    return existed


def load_keys(key_path=key_path):
    key_paths = os.listdir(key_path)
    key_paths.sort(key=lambda x: os.path.getctime(os.path.join(key_path, x)))
    keys = list()
    for device_id in key_paths:
        key_data = dict()
        key_data['device_id'] = device_id
        for name in ('cert', 'key', 'owner', 'serial'):
            with open(os.path.join(key_path, device_id, name)) as f:
                value = '\n'.join(f.readlines())
            key_data[name] = value
        keys.append(key_data)
    return keys


def remove_key(device_id, dry_run=False, key_path=key_path):
    path = os.path.join(key_path, device_id)
    if os.path.isdir(path):
        if not dry_run:
            shutil.rmtree(path)
            logger.debug('removed key:' + path)
    return path
