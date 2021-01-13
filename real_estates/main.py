import sys, json, webbrowser, os
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import QThread, QObject, Signal
from ui import Ui_MainWindow
from worker import Worker

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        #ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.startButton.clicked.connect(self.handleClicked)
        self.checkboxes = [self.ui.checkBox, self.ui.checkBox_2, self.ui.checkBox_3, self.ui.checkBox_4, self.ui.checkBox_5, self.ui.checkBox_6]
        
    
    def handleClicked(self):
        if not self.ui.locationInput.text():
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("지역을 설정해주세요.")
            
        else:
            filter = json.load(open("mod.json"))["filter"]
            filter_list = []
            for c in self.checkboxes:
                if c.isChecked():
                    filter_list.append(filter[c.text()])
            filter = ":".join(filter_list)
            #thread
            self.thread = QThread()
            self.worker = Worker(self.ui.locationInput.text(), filter)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progress.connect(self.ui.progressBar.setValue)
            self.thread.start()
            self.ui.startButton.setEnabled(False)
            self.thread.finished.connect(self.handleFinished)
    
    def handleFinished(self):
            self.ui.startButton.setEnabled(True)
            self.ui.progressBar.setValue(0)
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("수집이 완료되었습니다.")
            msgBox.setDefaultButton(QMessageBox.Ok)
            ret = msgBox.exec_()
            if ret == QMessageBox.Ok:
                path = os.getcwd()+"/result"
                webbrowser.open('file:///' + path)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
