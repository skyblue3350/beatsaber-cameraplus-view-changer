import sys
import time
import winreg
from pathlib import Path

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox

from ui.mainwindow import Ui_MainWindow
from ui.custom_ui.slider import CustomSlider
from ui.custom_ui.doubleslider import CustomDoubleSlider
from ui.custom_ui.checkbox import CustomCheckBox


class BeatsaberCameraPlusMod(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.initUi()

        self.cfg = self.getBeatsaberPath() / "cameraplus.cfg"
        self.preset = Path(__file__).resolve().cwd() / "preset"
        self.load()

        self.timer = QTimer(self)
        self.timer.setInterval(self.ui.spinBox.value() * 1000)
        self.timer.timeout.connect(self.changeItem)
        self.timer_id = None

    def initUi(self):
        ui = [
            CustomSlider("fov", 90, 80, 100),
            CustomSlider("antiAliasing", 2, 0, 4),
            CustomSlider("renderScale", 1, 0, 5),
            CustomSlider("positionSmooth", 10, 0, 20),
            CustomSlider("rotationSmooth", 5, 0, 20),
            CustomCheckBox("thirdPerson", True),
            CustomDoubleSlider("posx", 0, -5, 5),
            CustomDoubleSlider("posy", 2, -5, 5),
            CustomDoubleSlider("posz", -1.2, -5, 5),
            CustomDoubleSlider("angx", 15, -90, 180),
            CustomDoubleSlider("angy", 0, -180, 180),
            CustomDoubleSlider("angz", 0, -180, 180),
        ]

        for u in ui:
            u.valueChanged.connect(self.valueChanged)
            self.ui.verticalLayout.addWidget(u)

        self.ui.pushButton.clicked.connect(self.save)
        self.ui.checkBox.clicked.connect(self.switch)
        self.ui.listWidget.currentTextChanged.connect(self.selectItem)

    def outputData(self):
        while(True):
            try:
                f = self.cfg.open("w")

                for i in range(self.ui.verticalLayout.count()):
                    w = self.ui.verticalLayout.itemAt(i).widget()
                    f.write("{name}={value}".format(name=w.name, value=w.value))
                    f.write("\n")
            except PermissionError as e:
                continue
            else:
                f.close()
                break
            finally:
                f.close()

    def timerEvent(self, event):
        self.killTimer(self.timer_id)
        self.timer_id = None
        self.outputData()

    def valueChanged(self):
        # 書き込みチェックが入ってない時は何もしない
        if not self.ui.modifyWrite.isChecked():
            return

        if self.timer_id is None:
            self.outputData()

            # 短時間の連続書き込み防止
            self.timer_id = self.startTimer(1500)     



    def selectItem(self, text):
        with (self.preset / text).with_suffix(".cfg").open("r") as f:
            with self.cfg.open("w") as c:      
                c.write(f.read())

    def changeItem(self):
        self.timer.setInterval(self.ui.spinBox.value() * 1000)
        current = self.ui.listWidget.currentRow()
        count = self.ui.listWidget.count() - 1

        if count == 0:
            pass
        elif current == count:
            self.ui.listWidget.setCurrentRow(0)
        else:
           self.ui.listWidget.setCurrentRow(current + 1)

    def switch(self, isChecked):
        if isChecked:
            self.timer.start()
        else:
            self.timer.stop()

    def load(self):
        self.ui.listWidget.clear()
        for path in self.preset.glob("*.cfg"):
            self.ui.listWidget.addItem(path.stem)

    def save(self):
        name = self.ui.lineEdit.text()

        if name == "":
            QMessageBox.warning(self, "エラー", "プリセット名を指定して下さい")
            return

        with (self.preset / name).with_suffix(".cfg").open("w") as f:
            for i in range(self.ui.verticalLayout.count()):
                w = self.ui.verticalLayout.itemAt(i).widget()
                f.write("{name}={value}".format(name=w.name, value=w.value))
                f.write("\n")

        self.load()

    def getBeatsaberPath(self):
        path = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)

        info = winreg.QueryInfoKey(key)

        for i in range(info[0]):
            name = winreg.EnumKey(key, i)
            subkey = winreg.OpenKey(key, name)
            try:
                app, _ = winreg.QueryValueEx(subkey, "DisplayName")
            except FileNotFoundError as e:
                pass
            else:
                if "Beat Saber" in app:
                    path, _ = winreg.QueryValueEx(subkey, "InstallLocation")
                    return Path(path)


if __name__ == '__main__':
    myApp = QApplication(sys.argv)
    myWindow = BeatsaberCameraPlusMod()
    myWindow.show()
    myApp.exec_()
    sys.exit(0)