#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
from PyQt4 import QtGui,QtCore,Qt
from PyQt4.QtDeclarative import QDeclarativeView

class LoginForm(object):
    def setupUi(self, Form):
        Form.resize(350,210)
        self.verticalLayoutWidget = QtGui.QWidget(Form)
        # self.verticalLayoutWidget.resize(400, 270)
        Form.setCentralWidget(self.verticalLayoutWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(60, 50, 300, 160))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)

        self.font = QtGui.QFont()
        self.font.setPixelSize(14)   # 设置字号32,以像素为单位
        self.font.setFamily("SimSun")# 设置字体，宋体
        self.font.setFamily(u"微软雅黑")
        # self.font.setWeight(20)    # 设置字型,不加粗
        self.font.setBold(True)
        self.font.setItalic(False)   # 设置字型,不倾斜
        self.font.setUnderline(False)# 设置字型,无下划线
        self.setFont(self.font)     

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.verticalLayout.setMargin(0)

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.mailLabel = QtGui.QLabel('Usermail:',self.verticalLayoutWidget)
        self.horizontalLayout.addWidget(self.mailLabel)
        self.mailEdit = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.horizontalLayout.addWidget(self.mailEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.pwdLabel = QtGui.QLabel("Password:",self.verticalLayoutWidget)
        self.horizontalLayout_4.addWidget(self.pwdLabel)
        self.pwdEdit = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.horizontalLayout_4.addWidget(self.pwdEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()

        self.validateImgLayout = QtGui.QHBoxLayout()
        self.validateImg = QtGui.QLabel("                        ValidateImg")
        self.validateImgLayout.addWidget(self.validateImg)
        self.verticalLayout.addLayout(self.validateImgLayout)

        self.validateLabel = QtGui.QLabel('Validate:  ',self.verticalLayoutWidget)
        self.horizontalLayout_2.addWidget(self.validateLabel)
        self.validateEdit = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.horizontalLayout_2.addWidget(self.validateEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.pwdEdit.setEchoMode(QtGui.QLineEdit.Password)
        # self.pwdEdit.setMaxLength()

        self.horizontalLayout.setContentsMargins(40,0,40,0)
        self.horizontalLayout_2.setContentsMargins(40,0,40,0)
        self.horizontalLayout_4.setContentsMargins(40,0,40,0)

        self.mailEdit.setTextMargins(10,0, 10,0)
        self.pwdEdit.setTextMargins(10,0, 10,0)        
        self.validateEdit.setTextMargins(10,0, 10,0)

        # self.font.setPixelSize(14)
        # self.mailEdit.setFont(self.font)
        # self.pwdEdit.setFont(self.font)
        # self.validateEdit.setFont(self.font)

class LoginWindows(QtGui.QMainWindow,LoginForm):
    inputEnd = QtCore.pyqtSignal(str,str)
    validateInputEnd = QtCore.pyqtSignal(str) 
    def __init__(self):
        super(LoginWindows, self).__init__()
        self.setupUi(self)
        # #1f282e
        # 
        self.setStyleSheet('''
        /*搜索*/     
        .QWidget {
            background-color:#454e58;
            border-radius:0px;
        }
        QLineEdit {
            height: 21px;
            min-width: 190px;   
            max-width: 190px;
            min-height: 21px;
            max-height: 21px;
            padding: -5px;
            border: 7px;          
            border-image: url("img/nav_srch_input.png");              
        }
        QLabel{
            color:white;
        }
            ''')
        # border-image: url("img/nav_srch_input.png");
        # border-image: url("Resources/xmslider_track_high.tiff");

        self.showPwd()

        self.mailEdit.editingFinished.connect(self.mailEditEnd)
        self.pwdEdit.editingFinished.connect(self.pwdEditEnd)
        self.validateEdit.editingFinished.connect(self.validateEnd)
        self.inputEndFlag = False
        self.inputValidateEndFlag = False

    def validateEnd(self):
        if self.validateEdit.text():
            if not self.inputValidateEndFlag:
                self.inputValidateEndFlag = True
                self.validateEdit.setEnabled(False)
                self.validateInputEnd.emit(self.validateEdit.text())

    def mailEditEnd(self):
        self.mail = self.mailEdit.text()
        if self.mail:
            self.pwdEdit.setFocus()

    def pwdEditEnd(self):
        self.pwd = self.pwdEdit.text()
        if self.pwd:
            if self.mail:
                if not self.inputEndFlag:                    
                    self.inputEndFlag = True
                    self.mailEdit.setEnabled(False)
                    self.pwdEdit.setEnabled(False)
                    # inputOver
                    self.inputEnd.emit(self.mail,self.pwd)
            else:
                # mail not input
                self.mailEdit.setFocus()

    def inputValidate(self):
        self.inputValidateEndFlag = False
        self.validateEdit.setEnabled(True)
        self.validateEdit.clear()
        self.validateEdit.setFocus()
        self.validateImg.setPixmap(QtGui.QPixmap("Captcha.png"))
        self.showValidate()

    def emailPwdError(self):
        self.mailEdit.clear()
        self.pwdEdit.clear()
        self.mailEdit.setEnabled(True)
        self.pwdEdit.setEnabled(True)        
        self.mailEdit.setFocus()
        self.showPwd()

    def showValidate(self):
        self.validateLabel.setVisible(True);self.validateEdit.setVisible(True)
        self.validateImg.setVisible(True)
        self.mailLabel.setVisible(False);self.mailEdit.setVisible(False);
        self.pwdLabel.setVisible(False);self.pwdEdit.setVisible(False);

    def showPwd(self):
        self.inputEndFlag = False
        self.validateLabel.setVisible(False);self.validateEdit.setVisible(False)
        self.validateImg.setVisible(False)
        self.mailLabel.setVisible(True);self.mailEdit.setVisible(True);
        self.pwdLabel.setVisible(True);self.pwdEdit.setVisible(True);

class LoginThread(QtCore.QThread):
    def __init__(self):
        super(LoginThread, self).__init__()

    def run(self):
        pass
                
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    windows = LoginWindows()
    windows.show()
    sys.exit(app.exec_())