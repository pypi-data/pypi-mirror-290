import datetime
import pyqt_openai

from qtpy.QtCore import Qt
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import QDialog, QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QLabel

from pyqt_openai import APP_ICON, LICENSE_URL, GITHUB_URL, DISCORD_URL, APP_NAME, CONTACT
from pyqt_openai.lang.translations import LangClass
from pyqt_openai.widgets.linkLabel import LinkLabel


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle(LangClass.TRANSLATIONS['About'])
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)

        self.__okBtn = QPushButton(LangClass.TRANSLATIONS['OK'])
        self.__okBtn.clicked.connect(self.accept)

        p = QPixmap(APP_ICON)
        logoLbl = QLabel()
        logoLbl.setPixmap(p)

        descWidget1 = QLabel()
        descWidget1.setText(f'''
        <h1>{APP_NAME}</h1>
        Software Version {pyqt_openai.__version__}<br/><br/>
        © 2023 {datetime.datetime.now().year}. Used under the {pyqt_openai.LICENSE} License.<br/>
        Copyright (c) {datetime.datetime.now().year} {pyqt_openai.__author__}<br/>
        ''')

        descWidget2 = LinkLabel()
        descWidget2.setText(LangClass.TRANSLATIONS['Read MIT License Full Text'])
        descWidget2.setUrl(LICENSE_URL)

        descWidget3 = QLabel()
        descWidget3.setText(f'''
        <br/><br/>Contact: {CONTACT}<br/>
        <p>Powered by qtpy</p>
        ''')

        descWidget1.setAlignment(Qt.AlignmentFlag.AlignTop)
        descWidget2.setAlignment(Qt.AlignmentFlag.AlignTop)
        descWidget3.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.__githubLbl = LinkLabel()
        self.__githubLbl.setSvgFile(pyqt_openai.ICON_GITHUB)
        self.__githubLbl.setUrl(GITHUB_URL)

        self.__discordLbl = LinkLabel()
        self.__discordLbl.setSvgFile(pyqt_openai.ICON_DISCORD)
        self.__discordLbl.setUrl(DISCORD_URL)
        self.__discordLbl.setFixedSize(22, 19)

        lay = QHBoxLayout()
        lay.addWidget(self.__githubLbl)
        lay.addWidget(self.__discordLbl)
        lay.setAlignment(Qt.AlignmentFlag.AlignLeft)
        lay.setContentsMargins(0, 0, 0, 0)

        linkWidget = QWidget()
        linkWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(descWidget1)
        lay.addWidget(descWidget2)
        lay.addWidget(descWidget3)
        lay.addWidget(linkWidget)
        lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        lay.setContentsMargins(0, 0, 0, 0)

        rightWidget = QWidget()
        rightWidget.setLayout(lay)

        lay = QHBoxLayout()
        lay.addWidget(logoLbl)
        lay.addWidget(rightWidget)

        topWidget = QWidget()
        topWidget.setLayout(lay)

        cancelBtn = QPushButton(LangClass.TRANSLATIONS['Cancel'])
        cancelBtn.clicked.connect(self.close)

        lay = QHBoxLayout()
        lay.addWidget(self.__okBtn)
        lay.addWidget(cancelBtn)
        lay.setAlignment(Qt.AlignmentFlag.AlignRight)
        lay.setContentsMargins(0, 0, 0, 0)

        okCancelWidget = QWidget()
        okCancelWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(topWidget)
        lay.addWidget(okCancelWidget)

        self.setLayout(lay)

