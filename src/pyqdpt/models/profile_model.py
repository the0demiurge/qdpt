from PyQt5.QtCore import QStringListModel
from pyqdpt.utils import keys


class ProfileModel(QStringListModel):
    def __init__(self, keys=None):
        if keys is None:
            self.keys = list()
        else:
            self.keys = keys
        super(ProfileModel, self).__init__([self.getDescription(data) for data in self.keys])

    def appendData(self, key, device_id, serial, owner):
        self.appendKey(key, device_id, serial, owner)
        row = len(self.stringList())
        self.insertRow(row)
        self.setData(self.index(row), self.getDescription(self.keys[-1]))

    def deleteData(self, key, by='serial'):
        self.removeRow(self._getindex(key, by))
        self.delKey(key, by)

    def appendKey(self, key, device_id, serial, owner):
        keys.save_key(key, device_id, serial, owner)
        self.keys.append({
            'key': key,
            'device_id': device_id,
            'serial': serial,
            'owner': owner,
        })

    def getKey(self, key, by='serial'):
        return self.keys[self._getindex(key, by)]

    def delKey(self, key, by='serial'):
        self.keys.pop(self._getindex(key, by))

    def _getindex(self, key, by):
        if by == 'index':
            return key
        else:
            for index, item in enumerate(self.keys):
                if item.get(by) == key:
                    return index

    def getDescription(self, data):
        return ' -- '.join((data.get('owner'), data.get('serial')))
