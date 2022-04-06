# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTableWidget, QTableWidgetItem, QTextBrowser,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(995, 663)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.hLayout1 = QHBoxLayout()
        self.hLayout1.setObjectName(u"hLayout1")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.hLayout1.addWidget(self.label_2)

        self.comboNIC = QComboBox(self.centralwidget)
        self.comboNIC.setObjectName(u"comboNIC")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboNIC.sizePolicy().hasHeightForWidth())
        self.comboNIC.setSizePolicy(sizePolicy)
        self.comboNIC.setMinimumSize(QSize(30, 30))

        self.hLayout1.addWidget(self.comboNIC)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.hLayout1.addWidget(self.label)

        self.txtFilter = QLineEdit(self.centralwidget)
        self.txtFilter.setObjectName(u"txtFilter")
        self.txtFilter.setMinimumSize(QSize(0, 30))

        self.hLayout1.addWidget(self.txtFilter)

        self.btnStart = QPushButton(self.centralwidget)
        self.btnStart.setObjectName(u"btnStart")
        self.btnStart.setMinimumSize(QSize(0, 30))
        self.btnStart.setFlat(False)

        self.hLayout1.addWidget(self.btnStart)

        self.btnStop = QPushButton(self.centralwidget)
        self.btnStop.setObjectName(u"btnStop")
        self.btnStop.setMinimumSize(QSize(0, 30))

        self.hLayout1.addWidget(self.btnStop)


        self.verticalLayout.addLayout(self.hLayout1)

        self.tblFlows = QTableWidget(self.centralwidget)
        if (self.tblFlows.columnCount() < 7):
            self.tblFlows.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tblFlows.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tblFlows.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tblFlows.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tblFlows.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tblFlows.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tblFlows.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tblFlows.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.tblFlows.setObjectName(u"tblFlows")
        font = QFont()
        font.setPointSize(11)
        self.tblFlows.setFont(font)
        self.tblFlows.setAutoFillBackground(False)
        self.tblFlows.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tblFlows.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tblFlows.setSortingEnabled(True)
        self.tblFlows.setColumnCount(7)
        self.tblFlows.horizontalHeader().setVisible(True)
        self.tblFlows.horizontalHeader().setStretchLastSection(True)
        self.tblFlows.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.tblFlows)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.treeDetials = QTreeWidget(self.centralwidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeDetials.setHeaderItem(__qtreewidgetitem)
        self.treeDetials.setObjectName(u"treeDetials")
        font1 = QFont()
        font1.setPointSize(12)
        self.treeDetials.setFont(font1)
        self.treeDetials.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeDetials.setIndentation(20)
        self.treeDetials.header().setVisible(False)

        self.horizontalLayout.addWidget(self.treeDetials)

        self.txtHex = QTextBrowser(self.centralwidget)
        self.txtHex.setObjectName(u"txtHex")
        self.txtHex.setFont(font1)

        self.horizontalLayout.addWidget(self.txtHex)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 995, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SimpleSniffer", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Select NIC: ", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Filter: ", None))
        self.btnStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.btnStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        ___qtablewidgetitem = self.tblFlows.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"No.", None));
        ___qtablewidgetitem1 = self.tblFlows.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Time", None));
        ___qtablewidgetitem2 = self.tblFlows.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Source", None));
        ___qtablewidgetitem3 = self.tblFlows.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Destination", None));
        ___qtablewidgetitem4 = self.tblFlows.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Protocol", None));
        ___qtablewidgetitem5 = self.tblFlows.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Length", None));
        ___qtablewidgetitem6 = self.tblFlows.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Info", None));
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
    # retranslateUi

