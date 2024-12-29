# Form implementation generated from reading ui file '.\gui\designs\main_window.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(721, 531)
        self.central_widget = QtWidgets.QWidget(parent=MainWindow)
        self.central_widget.setObjectName("central_widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.central_widget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.camera_widget = QtWidgets.QWidget(parent=self.central_widget)
        self.camera_widget.setObjectName("camera_widget")
        self.horizontalLayout_3.addWidget(self.camera_widget)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.ip_addr = QtWidgets.QLineEdit(parent=self.central_widget)
        self.ip_addr.setText("")
        self.ip_addr.setMaxLength(15)
        self.ip_addr.setObjectName("ip_addr")
        self.verticalLayout.addWidget(self.ip_addr)
        self.password = QtWidgets.QLineEdit(parent=self.central_widget)
        self.password.setText("")
        self.password.setMaxLength(20)
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password.setObjectName("password")
        self.verticalLayout.addWidget(self.password)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.connect_btn = QtWidgets.QPushButton(parent=self.central_widget)
        self.connect_btn.setObjectName("connect_btn")
        self.horizontalLayout.addWidget(self.connect_btn)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.x_slider = QtWidgets.QSlider(parent=self.central_widget)
        self.x_slider.setMinimumSize(QtCore.QSize(188, 0))
        self.x_slider.setProperty("value", 50)
        self.x_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.x_slider.setObjectName("x_slider")
        self.horizontalLayout_2.addWidget(self.x_slider)
        self.y_slider = QtWidgets.QSlider(parent=self.central_widget)
        self.y_slider.setMinimumSize(QtCore.QSize(0, 188))
        self.y_slider.setProperty("value", 50)
        self.y_slider.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.y_slider.setObjectName("y_slider")
        self.horizontalLayout_2.addWidget(self.y_slider)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.verticalLayout_3.setStretch(2, 1)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_4.setStretch(0, 1)
        MainWindow.setCentralWidget(self.central_widget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.connect_btn.clicked.connect(MainWindow.connect) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RemoteCam"))
        self.ip_addr.setPlaceholderText(_translate("MainWindow", "IP address"))
        self.password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.connect_btn.setText(_translate("MainWindow", "Connect"))
