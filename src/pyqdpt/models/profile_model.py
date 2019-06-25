from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from pyqdpt.utils import keys


class ProfileTableModel(QStandardItemModel):
    def __init__(self, parent, keys=None):
        if keys is None:
            self.keys = list()
        else:
            self.keys = keys
        super(ProfileTableModel, self).__init__(len(self.keys), 2, parent)
        self.setHeaderData(0, Qt.Horizontal, 'owner')
        self.setHeaderData(1, Qt.Horizontal, 'serial')
        for row, key in enumerate(self.keys):
            self.setRowData(row, key)

    def appendItem(self, cert, key, device_id, serial, owner):
        existed = self.appendKey(cert, key, device_id, serial, owner)
        if existed:
            row = self._getindex(device_id, by='device_id')
        else:
            row = self.rowCount()
            self.insertRow(row)
        self.setRowData(row, self.keys[row])

    def deleteItem(self, key, by='serial'):
        self.removeRow(self._getindex(key, by))
        self.delKey(key, by)

    def setRowData(self, row, key):
        self.setData(self.index(row, 0), key['owner'])
        self.setData(self.index(row, 1), key['serial'])

    def appendKey(self, cert, key, device_id, serial, owner):
        existed = keys.save_key(cert, key, device_id, serial, owner)
        value = {
            'cert': cert,
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
        return ': '.join((data.get('owner'), data.get('serial')))

    def __len__(self):
        return self.rowCount()
