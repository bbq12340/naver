# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(480, 640)
        MainWindow.setStyleSheet(u"background-color: rgb(46, 48, 55);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.MainFrame = QFrame(self.centralwidget)
        self.MainFrame.setObjectName(u"MainFrame")
        self.MainFrame.setFrameShape(QFrame.NoFrame)
        self.MainFrame.setFrameShadow(QFrame.Plain)
        self.MainLabel = QLabel(self.MainFrame)
        self.MainLabel.setObjectName(u"MainLabel")
        self.MainLabel.setGeometry(QRect(0, 20, 451, 40))
        self.MainLabel.setStyleSheet(u"color: rgb(26, 192, 72);\n"
"font: 36pt \"Black Han Sans\";")
        self.MainLabel.setAlignment(Qt.AlignCenter)
        self.locationLabel = QLabel(self.MainFrame)
        self.locationLabel.setObjectName(u"locationLabel")
        self.locationLabel.setGeometry(QRect(190, 100, 80, 36))
        self.locationLabel.setStyleSheet(u"font: 13pt \"Black Han Sans\";")
        self.locationLabel.setAlignment(Qt.AlignCenter)
        self.startButton = QPushButton(self.MainFrame)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setGeometry(QRect(180, 390, 113, 32))
        self.startButton.setStyleSheet(u"QPushButton{\n"
"	background-color: rgb(0, 190, 36);\n"
"	color: rgb(255, 255, 255);\n"
"	font: 24pt \"Black Han Sans\";\n"
"}")
        self.optionFrame = QFrame(self.MainFrame)
        self.optionFrame.setObjectName(u"optionFrame")
        self.optionFrame.setGeometry(QRect(90, 210, 290, 101))
        self.optionFrame.setStyleSheet(u"")
        self.optionFrame.setFrameShape(QFrame.Panel)
        self.optionFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.optionFrame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.checkBox_6 = QCheckBox(self.optionFrame)
        self.checkBox_6.setObjectName(u"checkBox_6")
        self.checkBox_6.setAutoFillBackground(False)
        self.checkBox_6.setStyleSheet(u"color: rgb(255,255,255);")

        self.gridLayout.addWidget(self.checkBox_6, 1, 2, 1, 1)

        self.checkBox_4 = QCheckBox(self.optionFrame)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setAutoFillBackground(False)
        self.checkBox_4.setStyleSheet(u"color: rgb(255,255,255);")

        self.gridLayout.addWidget(self.checkBox_4, 1, 1, 1, 1)

        self.checkBox_2 = QCheckBox(self.optionFrame)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setAutoFillBackground(False)
        self.checkBox_2.setStyleSheet(u"color: rgb(255,255,255);")

        self.gridLayout.addWidget(self.checkBox_2, 1, 0, 1, 1)

        self.checkBox_5 = QCheckBox(self.optionFrame)
        self.checkBox_5.setObjectName(u"checkBox_5")
        self.checkBox_5.setAutoFillBackground(False)
        self.checkBox_5.setStyleSheet(u"color: rgb(255,255,255);")

        self.gridLayout.addWidget(self.checkBox_5, 0, 2, 1, 1)

        self.checkBox_3 = QCheckBox(self.optionFrame)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setAutoFillBackground(False)
        self.checkBox_3.setStyleSheet(u"color: rgb(255,255,255);")

        self.gridLayout.addWidget(self.checkBox_3, 0, 1, 1, 1)

        self.checkBox = QCheckBox(self.optionFrame)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setAutoFillBackground(False)
        self.checkBox.setStyleSheet(u"color: rgb(255,255,255);")

        self.gridLayout.addWidget(self.checkBox, 0, 0, 1, 1)

        self.locationInput = QLineEdit(self.MainFrame)
        self.locationInput.setObjectName(u"locationInput")
        self.locationInput.setGeometry(QRect(90, 140, 290, 30))
        self.locationInput.setStyleSheet(u"QLineEdit {\n"
"	border: 2px solid rgb(0, 190, 36);\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        self.progressBar = QProgressBar(self.MainFrame)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(0, 590, 451, 23))
        self.progressBar.setValue(0)

        self.verticalLayout.addWidget(self.MainFrame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\ub124\uc774\ubc84 \ubd80\ub3d9\uc0b0 \uc218\uc9d1\uae30", None))
        self.MainLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>NAVER <span style=\" color:#ffffff;\">\ubd80\ub3d9\uc0b0</span></p></body></html>", None))
        self.locationLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:24pt; color:#ffffff;\">\uc9c0\uc5ed\uba85</span></p></body></html>", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"\uc2dc\uc791", None))
        self.checkBox_6.setText(QCoreApplication.translate("MainWindow", u"\uc7ac\uac1c\ubc1c", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"\uc624\ud53c\uc2a4\ud154\ubd84\uc591\uad8c", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"\uc624\ud53c\uc2a4\ud154", None))
        self.checkBox_5.setText(QCoreApplication.translate("MainWindow", u"\uc7ac\uac74\ucd95", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"\uc544\ud30c\ud2b8\ubd84\uc591\uad8c", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"\uc544\ud30c\ud2b8", None))
        self.locationInput.setText("")
    # retranslateUi
