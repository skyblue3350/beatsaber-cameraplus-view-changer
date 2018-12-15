from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QSlider,
    QWidget,
)


class CustomDoubleSlider(QWidget):
    valueChanged = pyqtSignal()

    def __init__(self, name, default_value, min_value, max_value):
        super(CustomDoubleSlider, self).__init__()

        self.name = name
        self.default_value = default_value
        self.min_value = min_value
        self.max_value = max_value

        self.initUi()

    def initUi(self):
        self.layout = QHBoxLayout(self)
        self.label = QLabel(self.name, self)
        self.slider = QSlider(Qt.Horizontal, self)
        self.spin = QDoubleSpinBox(self)

        self.slider.valueChanged.connect(self.changeSlider)
        self.spin.valueChanged.connect(self.changeDoubleSpinBox)
        self.spin.valueChanged.connect(lambda: self.valueChanged.emit())

        self.spin.setSingleStep(0.1)
        self.spin.setRange(self.min_value, self.max_value)
        self.slider.setRange(self.min_value * 10, self.max_value * 10)
        self.slider.setValue(self.default_value * 10)

        self.layout.addWidget(self.label, 1)
        self.layout.addWidget(self.slider, 2)
        self.layout.addWidget(self.spin)

        self.setLayout(self.layout)

    def timerEvent(self, event):
        self.valueChanged.emit()
        self.stopTimer()

    def changeSlider(self, value):
        self.spin.setValue(value / 10.0)

    def changeDoubleSpinBox(self, value):
        self.slider.setValue(value * 10.0)

    @property
    def value(self):
        return self.spin.value()
