# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QMenuBar,
    QSizePolicy,
    QWidget,
)


class Ui_CondetrolMainWindow(object):
    def setupUi(self, CondetrolMainWindow):
        if not CondetrolMainWindow.objectName():
            CondetrolMainWindow.setObjectName("CondetrolMainWindow")
        CondetrolMainWindow.resize(800, 600)
        self.action_edit_device_configurations = QAction(CondetrolMainWindow)
        self.action_edit_device_configurations.setObjectName(
            "action_edit_device_configurations"
        )
        self.actionExport = QAction(CondetrolMainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionLoad = QAction(CondetrolMainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.action_edit_constants = QAction(CondetrolMainWindow)
        self.action_edit_constants.setObjectName("action_edit_constants")
        self.centralwidget = QWidget(CondetrolMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        CondetrolMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(CondetrolMainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.device_configurations_menu = QMenu(self.menubar)
        self.device_configurations_menu.setObjectName("device_configurations_menu")
        self.dock_menu = QMenu(self.menubar)
        self.dock_menu.setObjectName("dock_menu")
        CondetrolMainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.device_configurations_menu.menuAction())
        self.menubar.addAction(self.dock_menu.menuAction())
        self.device_configurations_menu.addAction(
            self.action_edit_device_configurations
        )

        self.retranslateUi(CondetrolMainWindow)

        QMetaObject.connectSlotsByName(CondetrolMainWindow)

    # setupUi

    def retranslateUi(self, CondetrolMainWindow):
        CondetrolMainWindow.setWindowTitle("")
        self.action_edit_device_configurations.setText(
            QCoreApplication.translate("CondetrolMainWindow", "Edit...", None)
        )
        self.actionExport.setText(
            QCoreApplication.translate("CondetrolMainWindow", "Export...", None)
        )
        self.actionLoad.setText(
            QCoreApplication.translate("CondetrolMainWindow", "Load...", None)
        )
        self.action_edit_constants.setText(
            QCoreApplication.translate("CondetrolMainWindow", "Edit...", None)
        )
        self.device_configurations_menu.setTitle(
            QCoreApplication.translate("CondetrolMainWindow", "Devices", None)
        )
        self.dock_menu.setTitle(
            QCoreApplication.translate("CondetrolMainWindow", "Docks", None)
        )

    # retranslateUi
