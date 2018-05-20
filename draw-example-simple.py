#!/usr/bin/env python
"""
Created on Fri Apr  6 00:02:12 2018
@author: frank
ref:
    https://wiki.python.org/moin/PyQt/Painting%20and%20clipping%20demonstration
    https://wiki.python.org/moin/PyQt/Painting%20and%20clipping%20demonstration?action=AttachFile&do=view&target=clipper.py
    https://wiki.python.org/moin/PyQt/Painting%20and%20clipping%20demonstration?action=AttachFile&do=get&target=clipper.py

"""

from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QFileDialog, QMessageBox, QProgressBar
from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout,QPushButton,QSizePolicy,QSplitter#, QCheckBox
from PyQt5.QtWidgets import QComboBox,QDialog, QLabel,QLineEdit#, QTableWidget,QStackedWidget
from PyQt5.QtWidgets import QDateTimeEdit,QDialogButtonBox
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtGui import QIcon,QFont,QKeySequence,QPolygon#,QVBoxLayout,QHBoxLayout
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread
from PyQt5.Qt import QDateTime
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QBrush
from PyQt5.QtCore import QSize, QLine, QPoint, QRect

class Window(QWidget):

    def __init__(self):
    
        QWidget.__init__(self)
        self.largest_rect = QRect(50, 50, 400, 400)
        
        self.clip_rect = QRect(50, 50, 400, 400)
        self.dragging = None
        self.drag_offset = QPoint()
        self.handle_offsets = (
            QPoint(8, 8), QPoint(-1, 8), QPoint(8, -1), QPoint(-1, -1)
            )
        
        self.path = QPainterPath()
        self.path.moveTo(100, 250)
        font = QFont()
        font.setPixelSize(80)
        self.path.addText(100, 300, font, "Clipping")
        
        self.polygon = QPolygon([QPoint(250, 100), QPoint(400, 250),
                                 QPoint(250, 400), QPoint(100, 250),
                                 QPoint(250, 100)])
    
    def paintEvent(self, event):
    
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QBrush(Qt.white))
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QBrush(Qt.red), 1, Qt.DashLine))
        painter.drawRect(self.largest_rect)
        painter.setPen(QPen(Qt.black))
        painter.drawRect(self.clip_rect)
        for i in range(4):
            painter.drawRect(self.corner(i))
        
        painter.setClipRect(self.clip_rect)
        painter.drawPolyline(self.polygon)
        painter.setBrush(QBrush(Qt.blue))
        painter.drawPath(self.path)
        painter.end()
    
    def corner(self, number):
    
        if number == 0:
            return QRect(self.clip_rect.topLeft() - self.handle_offsets[0], QSize(8, 8))
        elif number == 1:
            return QRect(self.clip_rect.topRight() - self.handle_offsets[1], QSize(8, 8))
        elif number == 2:
            return QRect(self.clip_rect.bottomLeft() - self.handle_offsets[2], QSize(8, 8))
        elif number == 3:
            return QRect(self.clip_rect.bottomRight() - self.handle_offsets[3], QSize(8, 8))
    
    def mousePressEvent(self, event):
    
        for i in range(4):
            rect = self.corner(i)
            if rect.contains(event.pos()):
                self.dragging = i
                self.drag_offset = rect.topLeft() - event.pos()
                break
        else:
            self.dragging = None
    
    def mouseMoveEvent(self, event):
    
        if self.dragging is None:
            return
        
        left = self.largest_rect.left()
        right = self.largest_rect.right()
        top = self.largest_rect.top()
        bottom = self.largest_rect.bottom()
        
        point = event.pos() + self.drag_offset + self.handle_offsets[self.dragging]
        point.setX(max(left, min(point.x(), right)))
        point.setY(max(top, min(point.y(), bottom)))
        
        if self.dragging == 0:
            self.clip_rect.setTopLeft(point)
        elif self.dragging == 1:
            self.clip_rect.setTopRight(point)
        elif self.dragging == 2:
            self.clip_rect.setBottomLeft(point)
        elif self.dragging == 3:
            self.clip_rect.setBottomRight(point)
        
        self.update()
    
    def mouseReleaseEvent(self, event):
    
        self.dragging = None
    
    def sizeHint(self):
        return QSize(500, 500)

import sys

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())