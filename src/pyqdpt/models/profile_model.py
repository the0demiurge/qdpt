from PyQt5.QtCore import QStringListModel
from pyqdpt.utils import keys


class ProfileModel(QStringListModel):
    def __init__(self, keys=None):
        if keys is None:
            self.keys = list()
        else:
            self.keys = keys
        super(ProfileModel, self).__init__([self.getDescription(data) for data in self.keys])

    def appendData(self, cert, key, device_id, serial, owner):
        existed = self.appendKey(cert, key, device_id, serial, owner)
        if existed:
            row = self._getindex(device_id, by='device_id')
        else:
            row = len(self.stringList())
            self.insertRow(row)
        self.setData(self.index(row), self.getDescription(self.keys[row]))

    def deleteData(self, key, by='serial'):
        self.removeRow(self._getindex(key, by))
        self.delKey(key, by)

    def appendKey(self, cert, key, device_id, serial, owner):
        existed = keys.save_key(cert, key, device_id, serial, owner)
        value = {
            'key': key,
            'device_id': device_id,
            'serial': serial,
            'owner': owner,
        }
        if existed:
            self.keys[self._getindex(device_id, by='device_id')] = value
        else:
            self.keys.append(value)
        return existed

    def getKey(self, key, by='serial'):
        return self.keys[self._getindex(key, by)]

    def delKey(self, key, by='serial'):
        deleted_key = self.keys.pop(self._getindex(key, by))
        keys.remove_key(deleted_key['device_id'])

    def _getindex(self, key, by):
        if by == 'index':
            return key
        else:
            for index, item in enumerate(self.keys):
                if item.get(by) == key:
                    return index

    def getDescription(self, data):
        return ' -- '.join((data.get('serial'), data.get('owner')))

    def __len__(self):
        return len(self.stringList())
