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
    save_path = os.path.join(key_path, serial)
    existed = os.path.exists(save_path)
    os.makedirs(save_path, exist_ok=True)
    for name, value in (
        ('cert', cert),
        ('key', key),
        ('owner', owner),
        ('serial', serial),
        ('device_id', device_id)
    ):
        with open(os.path.join(key_path, serial, name), 'w') as f:
            f.write(value)
    return existed


def load_keys(key_path=key_path):
    keys = list()
    if not os.path.exists(key_path):
        return keys
    key_paths = os.listdir(key_path)
    key_paths.sort(key=lambda x: os.path.getctime(os.path.join(key_path, x)))
    for path in key_paths:
        try:
            key_data = dict()
            for name in ('cert', 'key', 'owner', 'serial', 'device_id'):
                with open(os.path.join(key_path, path, name)) as f:
                    value = '\n'.join(f.readlines())
                key_data[name] = value
            keys.append(key_data)
        except Exception as e:
            logging.debug(e)
    return keys


def remove_key(serial, dry_run=False, key_path=key_path):
    path = os.path.join(key_path, serial)
    if os.path.isdir(path):
        if not dry_run:
            shutil.rmtree(path)
            logger.debug('removed key:' + path)
    return path
