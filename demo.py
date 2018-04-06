# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 00:02:12 2018

@author: stephen
"""

import sys

from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QFileDialog, QMessageBox, QProgressBar
from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout,QPushButton,QSizePolicy,QSplitter#, QCheckBox
from PyQt5.QtWidgets import QComboBox,QDialog, QLabel,QLineEdit#, QTableWidget,QStackedWidget
from PyQt5.QtWidgets import QDateTimeEdit,QDialogButtonBox
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtGui import QIcon,QFont,QKeySequence#,QVBoxLayout,QHBoxLayout
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread
from PyQt5.Qt import QDateTime
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage,QPixmap

import cv2
import os

class Thread(QThread):
    changePixmap = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.filepath = None
        self.width = 640
        self.height = 480

    def run(self):
        if not self.filepath:
            return
        
        cap = cv2.VideoCapture(os.path.abspath(self.filepath))
        while True:
            ret, frame = cap.read()
            if ret is False:
                break
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
            convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
            p = convertToQtFormat.scaled(self.width, self.height, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)
            
    def setpath(self,path):
        self.filepath = path
        
    def setsize(self,width,height):
        self.width,self.height = width,height

class CameraDisplay(QLabel):
  def __init__(self):
    super(CameraDisplay, self).__init__()

  def updateFrame(self, image):
    self.setPixmap(QPixmap.fromImage(image))
    
class Dialog(QDialog):
    up_camera_signal = QtCore.pyqtSignal(QImage)
    def __init__(self, parent = None):
        super(Dialog, self).__init__(parent)
        self.isfinished = False
        self.initialize()

    def act_fileopen(self):
        filepath,extensions = QFileDialog.getOpenFileName(self, r'File Open','',"Video files (*.avi *.mpeg *.mpg *.mp4)")
        self.thread.setpath(filepath)
        self.thread.start()
 
    def closeEvent(self, event):
        
        if self.isfinished:
            self.deleteLater()
            return
        
        reply = QMessageBox.question(self, 'warning',
                                     "Are you sure to quit dialog?", QMessageBox.Yes | 
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.thread.quit()
            self.deleteLater()
            event.accept()
        else:
            event.ignore()
            
    def initialize(self):
        ###
        self.up_camera = None
        ###
        '''
        up_camera = CameraDisplay()
        self.up_camera_signal.connect(up_camera.updateFrame)
        '''
        self.label = QLabel(self)
        #label.move(180, 120)
        self.label.resize(350, 350)
        button = QPushButton(self)
        button.setText('open')
        button.released.connect(self.act_fileopen)
        ###
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.label)
        vbox.addWidget(button)
        self.setLayout(vbox)
        ###
        self.thread = Thread(self)
        self.thread.changePixmap.connect(self.label.setPixmap)
        ###
        self.setMinimumSize(500,350)
        self.setWindowTitle("Demo")  
        self.show()

    def resizeEvent(self, event):
        #self.resized.emit()
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        self.thread.setsize(width-30,height-30)
        self.label.setGeometry(QtCore.QRect(0, height-20, width-20, 20))
        self.label.setVisible(True)
        self.update()
        return super(Dialog, self).resizeEvent(event)

if __name__ == "__main__":
    # Create an PyQT4 application object.
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    ex = Dialog()
    sys.exit(app.exec_())