from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QWidget,
)


class CustomCheckBox(QWidget):
    valueChanged = pyqtSignal()

    def __init__(self, name, default=False):
        super(CustomCheckBox, self).__init__()

        self.name = name
        self.default = default

        self.initUi()

    def initUi(self):
        self.layout = QHBoxLayout(self)
        self.label = QLabel(self.name, self)
        self.checkbox = QCheckBox(self)

        self.checkbox.setChecked(True)
        self.checkbox.stateChanged.connect(lambda: self.valueChanged.emit())

        self.layout.addWidget(self.label, 1)
        self.layout.addWidget(self.checkbox, 2)

        self.setLayout(self.layout)

    @property
    def value(self):
        return self.checkbox.isChecked()
