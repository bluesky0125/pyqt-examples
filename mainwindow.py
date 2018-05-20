#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 23:16:57 2017

@author: Frank

ref:http://pyqt.sourceforge.net/Docs/PyQt4/qkeysequence.html
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QFileDialog, QMessageBox, QProgressBar
from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout,QPushButton,QSizePolicy,QSplitter#, QCheckBox
from PyQt5.QtWidgets import QComboBox,QDialog, QLabel,QLineEdit#, QTableWidget,QStackedWidget
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtGui import QIcon,QFont,QKeySequence#,QVBoxLayout,QHBoxLayout
from PyQt5 import QtCore
#from PyQt5 import Qt
#from PyQt5.Qt import SIGNAL
import os
from misc import mkdir,switch,open_chrome

#from pictureflow import *#https://stackoverflow.com/questions/18024962/is-it-possible-to-preview-pdfs-in-a-pyqt-application
#import webbrowser#https://stackoverflow.com/questions/41919542/how-to-preview-pdf-file-in-browser-using-python

import time

class Crono(QtCore.QThread):
    tick = QtCore.pyqtSignal(int, name="changed") #New style signal

    def __init__(self, parent):
        QtCore.QThread.__init__(self,parent)

    def checkStatus(self):
        for x in range(1,101):
            self.tick.emit(x)                     
            time.sleep(1)
'''
class WTrainning(wMeta.WMeta, QtGui.QWidget):

    def __init__(self):
        super(WTrainning, self).__init__()
        self.crono = Crono()

    def createUI(self):
        #Create GUI stuff here

        #Connect signal of self.crono to a slot of self.progressBar
        self.crono.tick.connect(self.progressBar.setValue)
'''


        
class DocView(QMainWindow):
    #resized = QtCore.pyqtSignal()
    def __init__(self):
        super(DocView,self).__init__()
        #
        self.step = 0
        self.combos = {}# project member and other project-related people selection
        #
        self.lastpath = 'c:\\'
        self.filename = None
        self.isfinished = True
        self.isselected = False
        #
        self.filepath_in = None
        self.filepath_extract = None
        self.filepath_out = None
        #
        self.sections = None
        self.project_type = '水利'
        #
        self.address_dic = {}
        self.selected = 0
        #
        self.setting_info = {}
        #
        self.initUI()
    ####################################################################
    ############################UI#####################################
    ####################################################################        
    def createAct(self):
        ###########################
        # create act
        ###########################
        self.openAct = QAction(QIcon('icons\\open.png'), '打开', self)
        self.openAct.setShortcut('Ctrl+O')
        self.openAct.setStatusTip('Open Document')
        self.openAct.triggered.connect(self.act_open)
        ## exit
        self.exitAct = QAction(QIcon('icons\\close_.png'), '终了', self)
        self.exitAct.setShortcut('Ctrl+Q')
        self.exitAct.setStatusTip('Exit application')
        self.exitAct.triggered.connect(self.close)
        ## exit
        self.saveAct = QAction(QIcon('icons\\save.png'), '保存', self)
        self.saveAct.setShortcut('Ctrl+S')
        self.saveAct.setStatusTip('Save Document')
        self.saveAct.triggered.connect(self.act_save)
        ## select
        self.selectAct = QAction(QIcon('icons\\select.png'), '选择', self)
        self.selectAct.setShortcut('Ctrl+E')
        self.selectAct.setStatusTip('Select Project Member')
        self.selectAct.triggered.connect(self.act_select)
        ## delete
        self.deleteAct = QAction(QIcon('icons\\delete.png'), '选择', self)
        self.deleteAct.setShortcut('Ctrl+D')
        self.deleteAct.setStatusTip('Delete Document')
        self.deleteAct.triggered.connect(self.act_delete)
        ## extract 
        self.extractAct = QAction(QIcon('icons\\extract.png'), '提取', self)
        self.extractAct.setShortcut(QKeySequence('Ctrl+Shit+E'))
        self.extractAct.setStatusTip('Extract Format Pages')
        self.extractAct.triggered.connect(self.act_extract)
        ## split
        self.splitAct = QAction(QIcon('icons\\split.png'), '分离', self)
        self.splitAct.setShortcut('Ctrl+Shit+S')
        self.splitAct.setStatusTip('Split Document')
        self.splitAct.triggered.connect(self.act_split)
        ## fill 
        self.fillAct = QAction(QIcon('icons\\fillin.png'), '填写', self)
        self.fillAct.setShortcut('Ctrl+Shit+F')
        self.fillAct.setStatusTip('Fill in Blank')
        self.fillAct.triggered.connect(self.act_fillin)
        ## auto
        self.autoAct = QAction(QIcon('icons\\auto.png'), '完全自动', self)
        self.autoAct.setShortcut('Ctrl+Shit+A')
        self.autoAct.setStatusTip('Do Automatically')
        self.autoAct.triggered.connect(self.act_auto)
        ## merge
        self.mergeAct = QAction(QIcon('icons\\merge.png'), '合并', self)
        self.mergeAct.setShortcut('Ctrl+Shit+M')
        self.mergeAct.setStatusTip('Merge Documents')
        self.mergeAct.triggered.connect(self.act_merge)
        ## check
        self.todocxAct = QAction(QIcon('icons\\doc.png'), '检查', self)
        self.todocxAct.setShortcut('Ctrl+Shit+')
        self.todocxAct.setStatusTip('Check Document')
        self.todocxAct.triggered.connect(self.act_2docx)        
        ## 2xml
        self.toxmlAct = QAction(QIcon('icons\\xml.png'), '变换到XML', self)
        self.toxmlAct.setShortcut('Ctrl+Shit+X')
        self.toxmlAct.setStatusTip('Convert Docx to Xml')
        self.toxmlAct.triggered.connect(self.act_2xml)     
        ## 2html
        self.tohtmlAct = QAction(QIcon('icons\\html.png'), '变换到HTML', self)
        self.tohtmlAct.setShortcut('Ctrl+Shit+H')
        self.tohtmlAct.setStatusTip('Convert docx to HTML')
        self.tohtmlAct.triggered.connect(self.act_2html)                
        ## setting
        self.settingAct = QAction(QIcon('icons\\setting_.png'), '设置', self)
        self.settingAct.setShortcut('Ctrl+Shit+T')
        self.settingAct.setStatusTip('Setting')
        self.settingAct.triggered.connect(self.act_setting)
        ## help
        self.aboutAct = QAction(QIcon('icons\\help.png'), '关于', self)
        self.aboutAct.setShortcut('Ctrl+H')
        self.aboutAct.setStatusTip('About Program')
        self.aboutAct.triggered.connect(self.act_about)

    def createMenu(self):
        ###########################
        # create menu
        ###########################
        self.menubar = self.menuBar()
        ## File
        fileMenu = self.menubar.addMenu('&文件')
        fileMenu.addAction(self.openAct)
        fileMenu.addAction(self.saveAct)
        fileMenu.addAction(self.exitAct)
        ## Edit
        editMenu = self.menubar.addMenu('&编辑')
        editMenu.addAction(self.selectAct)
        ## Act
        processMenu = self.menubar.addMenu('&执行')
        processMenu.addAction(self.extractAct)
        processMenu.addAction(self.splitAct)
        processMenu.addAction(self.fillAct)
        processMenu.addAction(self.autoAct)
        processMenu.addAction(self.mergeAct)
        ## Tool
        toolMenu = self.menubar.addMenu('&工具')
        toolMenu.addAction(self.todocxAct)
        toolMenu.addAction(self.toxmlAct)
        toolMenu.addAction(self.tohtmlAct)
        ## Setting
        settingMenu = self.menubar.addMenu('&设置')
        settingMenu.addAction(self.settingAct)        
        ## Help
        helpMenu = self.menubar.addMenu('&帮助')
        helpMenu.addAction(self.aboutAct)
        
    def createToolbar(self):
        ###########################
        # create toolbar
        ###########################
        self.toolbar = self.addToolBar('File')
        self.toolbar.addAction(self.openAct)
        self.toolbar.addAction(self.saveAct)
        #self.toolbar.addAction(self.exitAct)
        #
        self.toolbar = self.addToolBar('Edit')
        self.toolbar.addAction(self.settingAct)
        self.toolbar.addAction(self.selectAct)
        #
        self.toolbar = self.addToolBar('Act')
        self.toolbar.addAction(self.extractAct)
        self.toolbar.addAction(self.splitAct)
        self.toolbar.addAction(self.fillAct)
        self.toolbar.addAction(self.autoAct)
        self.toolbar.addAction(self.mergeAct)
        #
        self.toolbar = self.addToolBar('Tool')
        self.toolbar.addAction(self.todocxAct)
        self.toolbar.addAction(self.toxmlAct)
        self.toolbar.addAction(self.tohtmlAct)
        #
        #self.toolbar = self.addToolBar('Setting')
        #self.toolbar.addAction(self.settingAct)
        #
        self.toolbar = self.addToolBar('Delete')
        self.toolbar.addAction(self.deleteAct)
        ####
        # create combobox
        self.toolbar = self.addToolBar('Select Target')
        self.combobox = QComboBox()
        self.combobox.currentIndexChanged.connect(self.selection_change)
        self.combobox.setMinimumWidth(150)
        self.combobox.setMinimumHeight(20)
        self.toolbar.addWidget(self.combobox)
        # create progress bar
        self.toolbar = self.addToolBar('Progress')
        
        self.progressBar = QProgressBar(self)
        self.progressBar.setEnabled(True)
        #width = self.frameGeometry().width()
        #height = self.frameGeometry().height()
        #self.progressBar.setGeometry(0, height-20, width-20, 20)
        self.progressBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.progressBar.setValue(self.step)
        #self.setCentralWidget(self.progressBar)
        self.timer = QtCore.QBasicTimer()
        self.timer.start(20, self)
        self.toolbar.addWidget(self.progressBar)

    def createDlgs(self):
        ###################################
        ##### select #######################
        ###################################
        self.dlg_select = QDialog(self)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        for position in []:#POSITION:
            label = QLabel()
            label.setText(position)
            label.setMinimumWidth(80)
            combo = QComboBox()
            print(position)
            for case in switch(position):
                if case('法人'):
                    positions = ['项目经理']
                    break
                if case('联系人'):
                    positions = ['工程师']
                    break
                if case('委托人1'):
                    positions = ['项目经理','工程师']
                    break
                if case('委托人2'):
                    positions = ['项目经理','工程师']
                    break
                if case('技术负责人'):
                    positions = ['工程师']
                    break
                if case('财务负责人'):
                    positions = ['工程师']
                    break
                if case():
                    positions = [position]
                    break
            print(positions)
            from db_sqlite import get_name_list
            combo.addItems(get_name_list(positions))#db['human'].filtering_by_position(positions=positions))
            combo.setMinimumWidth(90)
            self.combos[position] = combo
            hbox = QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(label)
            hbox.addWidget(combo)
            vbox.addLayout(hbox)
        self.refresh_project_members()
        self.dlg_select.setLayout(vbox)
        self.dlg_select.setWindowTitle(r'选择项目有关人')
        self.dlg_select.setWindowIcon(QIcon('icons\\select.png'))
        ######################################
        ### setting ##########################
        ######################################
        self.dlg_setting = QDialog(self)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        #####################################
        from db_sqlite import get_project_types
        label = QLabel()
        label.setText('项目类型')
        label.setMinimumWidth(80)
        combo = QComboBox()
        for ptype in get_project_types():
            combo.addItem(ptype)
        combo.setMinimumWidth(90)
        self.ptype_combo = combo
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(label)
        hbox.addWidget(self.ptype_combo)
        vbox.addLayout(hbox)
        ############################
        ############################
        self.setting_labels = []
        self.setting_buttons = []
        self.setting_edits = []
        self.setting_selected = 0
        for i,routine in enumerate(PATH):
            label = QLabel()
            label.setText(routine)
            label.setMinimumWidth(80)
            self.setting_labels.append(label)
            edit = QLineEdit()
            if routine in list(db.keys()):
                edit.setText(db[routine])
                self.setting_info[PATH[i]] = db[routine]
            edit.setMinimumWidth(200)
            self.setting_edits.append(edit)
            
            button = QPushButton()
            self.setting_buttons.append(button)
            self.setting_buttons[i].setText('选择')
            self.setting_buttons[i].toggle()
            self.setting_buttons[i].setAccessibleName(str(i))
            self.setting_buttons[i].released.connect(self.act_filebrowser)
            #self.connect(button,SIGNAL("clicked()"),self.act_filebrowser)
            #button.clicked.connect(lambda:self.act_filebrowser(button))
            #self.setting_buttons.append(button)
            #self.setting_buttons[i].clicked.connect(lambda:self.act_filebrowser(self.setting_buttons[i]))
            hbox = QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(label)
            hbox.addWidget(edit)
            hbox.addWidget(button)
            vbox.addLayout(hbox)
        self.dlg_setting.setLayout(vbox)
        self.dlg_setting.setWindowTitle(r'选择路径')
        self.dlg_setting.setWindowIcon(QIcon('icons\\setting_.png'))        

    @staticmethod
    def createTextEdit():
        textEdit = QTextEdit()
        textEdit.setFont(QFont('宋体',16))
        return textEdit
    
    @staticmethod
    def createWebView():
        webView = QWebView()
        webView.settings().setAttribute(QWebSettings.PluginsEnabled, True)
        #self.webView.settings().setAttribute(QWebSettings.WebAttribute.DeveloperExtrasEnabled, True)
        webView.settings().setAttribute(QWebSettings.PrivateBrowsingEnabled, True)
        webView.settings().setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)
        #self.webView.loadFinished.connect(self._loadfinished)
        #self.webView.setUrl(QtCore.QUrl("file:///G:/AutoMaking/src/Documentation/test.pdf"))
        #self.webView.load(QtCore.QUrl().fromLocalFile("G:\\AutoMaking\\src\\Documentation\\test.pdf"))
        #`self.webView.setHtml('<html><head></head><title></title><body></body></html>', baseUrl = QtCore.QUrl().fromLocalFile("G:\\AutoMaking\\src\\Documentation\\test.pdf"))
        #webView.setHtml(docx2html("G:\\AutoMaking\\src\\Documentation\\test.docx"))
        #self.webView.show()
        #self.webView.hide()
        #self.webView.setObjectName("webView")
        #QtCore.QTimer.singleShot(1200, self.webView.show)
        #self.webView.setContent()
        return webView
    
    def createViews(self):
        
        self.preView_L = DocView.createTextEdit()#createWebView()
        self.preView_L.setObjectName('TextEdit_L')#'WebView_L'
        self.preView_L.setAccessibleName('TextEdit_L')
        self.preView_R = DocView.createTextEdit()#createWebView()
        self.preView_R.setObjectName('TextEdit_R')#'WebView_R'
        self.preView_R.setAccessibleName('TextEdit_R')
        
        self.splitter = QSplitter(QtCore.Qt.Horizontal)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.addWidget(self.preView_L)
        self.splitter.addWidget(self.preView_R)
        self.setCentralWidget(self.splitter)
        
    def initUI(self):
        # create act
        self.createAct()                
        # create status bar
        self.statusBar()            
        # create menu
        self.createMenu()
        # create toolbar
        self.createToolbar()
        # create dlgs
        self.createDlgs()
        # create central widgets
        self.createViews()
        
        # set size
        #self.setGeometry(300, 300, 350, 250)
        #self.resized.connect(self.act_resize)
        self.setMinimumSize(500,350)
        self.showMaximized()
        self.setWindowTitle(r'标书自动生成')# set title
        self.setWindowIcon(QIcon('icons\\document_.png'))# set windowIcon
        self.show()
        ##
        #self.setMouseTracking(True)
    ####################################################################
    ##############################Signals################################
    ####################################################################
    '''
    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.rubberband.setGeometry(
            QtCore.QRect(self.origin, QtCore.QSize()))
        self.rubberband.show()
        QtGui.QWidget.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if self.rubberband.isVisible():
            self.rubberband.setGeometry(
                QtCore.QRect(self.origin, event.pos()).normalized())
        QtGui.QWidget.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        if self.rubberband.isVisible():
            self.rubberband.hide()
            selected = []
            rect = self.rubberband.geometry()
            for child in self.findChildren(QtGui.QPushButton):
                if rect.intersects(child.geometry()):
                    selected.append(child)
            print 'Selection Contains:\n ',
            if selected:
                print '  '.join(
                    'Button: %s\n' % child.text() for child in selected)
            else:
                print ' Nothing\n'
        QtGui.QWidget.mouseReleaseEvent(self, event)
    '''
    
    def resizeEvent(self, event):
        #self.resized.emit()
        '''
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        print(width,height)
        self.progressBar.setGeometry(QtCore.QRect(0, height-20, width-20, 20))
        self.progressBar.setVisible(True)
        self.update()
        '''
        return super(DocView, self).resizeEvent(event)
    
    def timerEvent(self, e):
      
        if self.step >= 100:        
            self.timer.stop()
            return
            
        self.step = self.step + 1
        self.progressBar.setValue(self.step)
        
    def keyPressEvent(self, event):
        #
        if event.key() ==  QtCore.Qt.Key_Escape: # QtCore.Qt.Key_Escape is a value that equates to what the operating system passes to python from the keyboard when the escape key is pressed.
            self.close()
        
    def closeEvent(self, event):
        
        if self.isfinished:
            self.deleteLater()
            return
        
        reply = QMessageBox.question(self, '警示',
                                     "确定关闭?", QMessageBox.Yes | 
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.deleteLater()
            event.accept()
        else:
            event.ignore()
            
    def selection_change(self,i):
        '''
        print("Items in the list are :")
		
        for count in range(self.combobox.count()):
            print(self.combobox.itemText(count))
        print("Current index",i,"selection changed ",self.combobox.currentText())
        '''
        section_name = self.combobox.currentText()
        print(section_name)
        if '提取的文件' == section_name:
            inpath = self.filepath_extract
            outpath = None
        elif '原件' == section_name:
            inpath = self.filepath_in
            outpath = self.filepath_out
        else:
            inpath = os.path.join(self.split_dir,section_name+'.docx')
            outpath = os.path.join(self.processed_dir,section_name+'.docx')
        self.refresh_left_preview(inpath)
        self.refresh_right_preview(outpath)
    ####################################################################
    ##############################Actions################################
    ####################################################################
    '''
    def act_resize(self):
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        self.progressBar.setGeometry(0, height-40, width-20, 20)
    '''    
    def act_open(self):
        filepath,extensions = QFileDialog.getOpenFileName(self, r'打开招标文件','',"Document files (*.docx *.doc *.wps *pdf)")
        print(filepath)
        if filepath is self.filepath_in:
            return
        if filepath is not '':
            self.lastpath,self.filename = os.path.split(filepath)
            filename,extension = os.path.splitext(filepath)
            self.filepath_in = filename + '.docx'
            self.filepath_extract = os.path.join(self.lastpath,'extracted.docx')
            self.filepath_out = os.path.join(self.lastpath,'out.docx')
            self.address_dic = {}
            if '.docx' in extension:
                self.combobox.clear()
                self.combobox.addItem('原件')
                return
            else:
                reply = QMessageBox.question(self, '警示',
                             "变换文件扩展名?", QMessageBox.Yes |
                             QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.No:
                    QMessageBox.warning(self,'警示','文件扩展名需要被变换')
                    return
            self.combobox.clear()
            self.combobox.addItem('原件')
            # convert into docx file        
            for case in switch(extension):
                if case('.doc'):
                    doc2docx(filepath)
                    break
                if case('.pdf'):
                    pdf2docx(filepath)
                    break
                if case(''):
                    break

    def act_select(self):
        self.dlg_select.show()
        self.refresh_project_members()
        from processing.xml2dict import dic2xml
        dic2xml(self.setting_info,os.path.join(os.getcwd(),'db\\项目设置.xml'))
        from setting import set_xml_db
        set_xml_db()
        '''
        self.dlg_select.show()
        #
        self.refresh_project_members()
        #
        db['finance'].filtering(need_years=3)
        #db['human'].select_people(name_list=[db['project_members'][position] for position in POSITION])
        db['projects_done'].filtering(project_types=['水利'],need_years=3)
        db['projects_being'].filtering(project_types=['水利'])
        '''
        #
    
    def act_extract(self):
        if self.filepath_in is None or not os.path.exists(self.filepath_in):
            self.act_open()
        # initialize
        self.combobox.clear()
        self.combobox.addItem('原件')
        self.combobox.addItem(r'提取的文件')
        self.combobox.setCurrentIndex(1)
        # 
        extract = Extract(self.filepath_in)
        extract.process(output_filepath=self.filepath_extract)
        #db['project_info'].set_db(extract.extract_project_infos())
        self.refresh_left_preview(self.filepath_extract)
        #self.isfinished = True
        #
    
    def act_split(self):
        mkdir(self.split_dir)
        split = Split(input_filepath=self.filepath_extract)
        self.sections = split.process(self.progressBar)
        self.combobox.addItems(self.sections)
    
    def act_fillin(self):
        self.refresh_project_members()
        #https://stackoverflow.com/questions/6415737/change-the-value-of-the-progress-bar-from-a-class-other-than-my-gui-class-pyqt4?rq=1
        section_name = self.combobox.currentText()
        #print(section_name)
        if any(key in section_name for key in ['提取的文件','原件']):
            QMessageBox.about(self,'通知','请先选择要填写的')
            return
        # set in and out path
        print(self.processed_dir)
        if not os.path.exists(self.processed_dir):
            os.mkdir(self.processed_dir)
        inpath = os.path.join(self.split_dir,section_name+'.docx')
        outpath = os.path.join(self.processed_dir,section_name+'.docx')
        # fillin
        if not os.path.exists(outpath):
            fillin = FillIn(inpath)
            fillin.process(outpath)
        # preview
        self.refresh_right_preview(outpath)

    def act_auto(self):
        self.refresh_project_members()
        self.progressBar.setValue(0)
        mkdir(self.processed_dir)
        count = len(self.sections)
        for index,section in enumerate(self.sections):
            fillin = FillIn(os.path.join(self.split_dir,section+'.docx'))
            fillin.process(os.path.join(self.processed_dir,section+'.docx'))
            self.progressBar.setValue(int((index+1)*100/count))
        
    def act_merge(self):
        merge = Merge(tmpdir=self.processed_dir,section_names=self.sections)
        merge.process(self.filepath_out)
        opendocument(self.filepath_out)

    def act_delete(self):
        section_name = self.combobox.currentText()
        #print(section_name)
        if '原件' == section_name:
            filepath = self.filepath_out
        elif '提取的文件' == section_name:
            filepath = self.filepath_extract
        else:
            filepath = os.path.join(self.processed_dir,section_name+'.docx')

        if os.path.exists(filepath):
             os.remove(filepath)
             self.refresh_right_preview(filepath)
            
    def act_save(self):
        filepath,extensions = QFileDialog.getSaveFileName(self, r'保存投标文件','',"Document files (*.docx)")
        if os.path.exists(filepath):
            os.rename(self.filepath_out,filepath)
        pass

    def act_2docx(self):
        section_name = self.combobox.currentText()
        #print(section_name)
        if '原件' == section_name:
            outpath = self.filepath_out
            inpath = self.filepath_in            
        elif '提取的文件' == section_name:
            outpath = self.filepath_extract
            inpath = None
        else:
            outpath = os.path.join(self.processed_dir,section_name+'.docx')
            inpath = os.path.join(self.split_dir,section_name+'.docx')

        if os.path.exists(outpath):
            opendocument(outpath)
        elif outpath is not None and os.path.exists(inpath):
            opendocument(inpath)

                
    def act_2xml(self):
        section_name = self.combobox.currentText()
        if '原件' == section_name:
            inpath = self.filepath_in
        elif '提取的文件' == section_name:
            inpath = self.filepath_extract
        else:
            if os.path.exists(os.path.join(self.processed_dir,section_name+'.docx')):
                inpath = os.path.join(self.processed_dir,section_name+'.docx')
            else:
                inpath = os.path.join(self.split_dir,section_name+'.docx')
        outpath = os.path.splitext(inpath)[0] + '.xml'
        if not os.path.exists(outpath):
            docx2xml(inpath)
        open_chrome(outpath)

    def act_2html(self):
        section_name = self.combobox.currentText()
        if '原件' == section_name:
            inpath = self.filepath_in
        elif '提取的文件' == section_name:
            inpath = self.filepath_extract
        else:
            if os.path.exists(os.path.join(self.processed_dir,section_name+'.docx')):
                inpath = os.path.join(self.processed_dir,section_name+'.docx')
            else:
                inpath = os.path.join(self.split_dir,section_name+'.docx')
        outpath = os.path.splitext(inpath)[0] + '.html'
        if not os.path.exists(outpath):
            docx2html(inpath)
        open_chrome(outpath)
        
    def act_about(self):
        QMessageBox.about(self,'关于标书自动生成软件','版本号：0.1.0\n生成时间：2017.11.28')
    
    def act_setting(self):
        self.dlg_setting.show()
        self.setting_info['项目类型'] = self.ptype_combo.currentText()
        from processing.xml2dict import dic2xml
        dic2xml(self.setting_info,os.path.join(os.getcwd(),'db\\项目设置.xml'))
        from setting import set_xml_db
        set_xml_db()
        
    def act_filebrowser(self):#,button):
        #print(selected)
        sending_button = self.sender()
        selected = int(sending_button.accessibleName())#int(button.accessibleName())#self.setting_buttons.index(button)#int(object.accessibleName())
        dir_path = str(QFileDialog.getExistingDirectory(self, PATH[selected])) if '数据库' not in PATH[selected] else QFileDialog.getOpenFileName(self, PATH[selected],'',"sqlite database files (*.db)")[0]
        if dir_path is not None and dir_path is not '':
            print(dir_path)
            db[PATH[selected]] = dir_path
            self.setting_edits[selected].setText(dir_path)
            self.setting_info[PATH[selected]] = dir_path
        #print(dir_path)
    ####################################################################
    ##############################Methods################################
    #################################################################### 
    def refresh_project_members(self):
        project_member_info = {}
        for position in POSITION:
            project_member_info[position] = self.combos[position].currentText()
        self.setting_info['项目组织机构'] = project_member_info
        '''
        for position in POSITION:
            db['project_members'][position] = self.combos[position].currentText()
        if len(db['project_members']) > 0:
            db['human'].select_people(name_list=[db['project_members'][position] for position in POSITION])
        #print(self.project_members)
        '''
        
    def _loadfinished(self,ok):
        #self.webView.load(QtCore.QUrl('about:blank'))
        pass
    
    def refresh_left_preview(self,filepath):
        if filepath and os.path.exists(filepath):
            #print(self.preView_L.accessibleName(),self.preView_L.objectName(),'here')
            if 'Edit' in self.preView_L.accessibleName():
                fulltext = docx2text(filepath)
                self.preView_L.setText(fulltext)
            else:
                self.preView_L.setHtml(docx2html(filepath))
    
    def refresh_right_preview(self,filepath):
        if filepath and os.path.exists(filepath):
            if 'Edit' in self.preView_R.accessibleName():
                fulltext = docx2text(filepath)
                self.preView_R.setText(fulltext)
            else:
                self.preView_R.setHtml(docx2html(filepath))
        else:
            if 'Edit' in self.preView_L.accessibleName():
                self.preView_R.setText('')
            else:
                self.preView_R.setHtml('')            
        
if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    ex = DocView()
    sys.exit(app.exec_())