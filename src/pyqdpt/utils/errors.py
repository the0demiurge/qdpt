from PyQt5.QtWidgets import QMessageBox


class ErrorBox(QMessageBox):
    def __init__(self, text, informative, detail='', retry=False, retry_connect=None):
        super(ErrorBox, self).__init__()
        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle("Error!")
        self.setText(text)
        self.setInformativeText(informative)
        if detail:
            self.setDetailedText(detail)
        if retry:
            self.setStandardButtons(QMessageBox.Retry | QMessageBox.Ok)
        self.setDefaultButton(QMessageBox.Ok)
