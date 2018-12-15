from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QSlider, QHBoxLayout, QLabel, QSpinBox


class CustomSlider(QWidget):
    valueChanged = pyqtSignal()
    def __init__(self, name, default_value, min_value, max_value):
        super(CustomSlider, self).__init__()

        self.name = name
        self.default_value = default_value
        self.min_value = min_value
        self.max_value = max_value

        self.initUi()

    def initUi(self):
        self.layout = QHBoxLayout(self)
        self.label = QLabel(self.name, self)
        self.slider = QSlider(Qt.Horizontal, self)
        self.spin = QSpinBox(self)

        self.slider.valueChanged.connect(self.spin.setValue)
        self.spin.valueChanged.connect(self.slider.setValue)
        self.spin.valueChanged.connect(lambda: self.valueChanged.emit())

        self.spin.setRange(self.min_value, self.max_value)
        self.slider.setRange(self.min_value, self.max_value)
        self.slider.setValue(self.default_value)


        self.layout.addWidget(self.label, 1)
        self.layout.addWidget(self.slider, 2)
        self.layout.addWidget(self.spin)

        self.setLayout(self.layout)

    @property
    def value(self):
        return self.spin.value()