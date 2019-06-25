import os
import traceback

from PyQt5.QtWidgets import QDialog, QMessageBox

from pyqdpt import utils
from pyqdpt.static import connection_help_url
from pyqdpt.utils.errors import ErrorBox
from pyqdpt.views.ui_register import Ui_RegistDialog


class RegisterDialog(QDialog):
    def __init__(self):
        super(RegisterDialog, self).__init__()
        self.ui = Ui_RegistDialog()
        self.ui.setupUi(self)
        self.register_session = None
        self.value = None

        self.ui.startButton.clicked.connect(self.startUSBNetwork)
        self.ui.requestButton.clicked.connect(self.request)
        self.ui.codeButton.clicked.connect(self.auth)
        self.ui.scanButton.clicked.connect(self.startScan)
        self.ui.helpButton.clicked.connect(self.helpConnect)

    def startScan(self):
        self.ui.scanButton.setDisabled(True)
        try:
            ip, iface, dev = utils.connect.main()
        except Exception as e:
            ErrorBox(
                'Scan failed!',
                'ErrorMsg: {}'.format(e),
                traceback.format_exc(),
            ).exec()
            self.ui.scanButton.setEnabled(True)
            return
        for button, text in (
            (self.ui.devInput, dev),
            (self.ui.ipInput, ip),
            (self.ui.ifaceInput, iface),
        ):
            if text:
                button.setText(text)
        self.request()
        self.ui.scanButton.setEnabled(True)

    def startUSBNetwork(self):
        dev = self.ui.devInput.text()
        if not os.path.exists(dev):
            ErrorBox(
                'Device does not exist:"{}"'.format(dev),
                'Press "Help" button for more information',
                '\n'.join([i for i in os.listdir('/dev') if i.startswith('tty')])
            ).exec()
            return

        if not dev.startswith('/dev/tty'):
            answer = QMessageBox.warning(
                self,
                'Warning',
                '\n'.join([
                    '<b>Danger!</b> Device "{}" is not the format with "/dev/ttyXXXX"'.format(dev),
                    'This may cause lost of data, continue?'
                ]),
                QMessageBox.No | QMessageBox.Yes, QMessageBox.No
            )
            if answer != QMessageBox.Yes:
                return

        method = self.ui.methodBox.currentText()
        self.ui.startButton.setDisabled(True)
        try:
            utils.start_usb_ethernet(method, dev)
            QMessageBox.information(
                self,
                'Started',
                'USB network started with device "{}" and method "{}"'.format(dev, method),
            )
        except Exception as e:
            ErrorBox(
                'USB Network start failed!'
                'ErrorMsg:{}'.format(e),
                traceback.format_exc()
            )
        self.ui.startButton.setEnabled(True)

    def request(self):
        self.ui.requestButton.setDisabled(True)
        ip = self.ui.ipInput.text()
        iface = self.ui.ifaceInput.text()
        addr = '[{}%{}]'.format(ip, iface)
        try:
            self.client = utils.DigitalPaper(addr)
        except Exception as e:
            ErrorBox(
                'IP or iface wrong!',
                'ErrorMsg: {}'.format(e),
                traceback.format_exc(),
            ).exec()
            self.ui.requestButton.setEnabled(True)
            return
        try:
            self.register_session = self.client.register()
            next(self.register_session)
        except Exception as e:
            ErrorBox(
                'Register request failed!',
                'ErrorMsg: {}'.format(e),
                traceback.format_exc(),
            ).exec()
            self.ui.requestButton.setEnabled(True)
            return
        QMessageBox.information(
            self,
            'Code',
            'Please put in the authentication code downside',
        )
        self.ui.requestButton.setEnabled(True)

    def auth(self):
        self.ui.codeButton.setDisabled(True)
        if self.register_session is None:
            QMessageBox.information(
                self,
                'Auth failed'
                'Press "Request" button first'
            )
        pin = self.ui.codeInput.text()

        try:
            self.key_data = self.register_session.send(pin)
        except StopIteration as s:
            cert, key, device_id = s.value
            self.client.authenticate(device_id, key)
            owner = self.client.get_owner()
            info = self.client.get_info()
            serial = info['serial_number']
            self.value = {
                'cert': cert,
                'key': key,
                'device_id': device_id,
                'serial': serial,
                'owner': owner,
            }
            QMessageBox.information(
                self,
                'Success',
                'Device{}: {} successfully added!'.format(owner, serial)
            )
            self.hide()
            return self.value
        except Exception as e:
            ErrorBox(
                'Authencation failed!',
                'ErrorMsg: {}'.format(e),
                traceback.format_exc(),
            ).exec()
            return
        finally:
            self.ui.codeButton.setEnabled(True)

    def helpConnect(self):
        QMessageBox.information(
            self,
            'Help',
            'For connection help, access this url:<br><a href="{url}">{url}</a>'.format(url=connection_help_url)
        )


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    dia = RegisterDialog()
    dia.exec()
