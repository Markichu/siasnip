import sys
import pyperclip
import configparser
import ctypes
from time import sleep
from siaskynet import Skynet
from playsound import playsound
from PyQt5 import QtWidgets, QtCore, QtGui
from PIL import Image
from desktopmagic.screengrab_win32 import saveRectToBmp

config = configparser.ConfigParser()
config.read('cfg.ini')

uploadportal = config['config']['uploadportaladdress']
linkportal = config['config']['linkportaladdress']
beepname = config['config']['beepfilename']

def upload(file):
    # upload file to skynet
    print('uploading to skynet')
    opts = Skynet.default_upload_options
    opts.portalUrl = uploadportal
    skylink = Skynet.UploadFile(file)
    # put link into clipboard
    pyperclip.copy(linkportal + '/' + Skynet.strip_prefix(skylink))
    print('upload finished')
    # beep
    playsound(beepname, False)
    # wait for sound to play then close
    sleep(3)

class SnipWindow(QtWidgets.QWidget):
    def __init__(self):
        super(SnipWindow, self).__init__()

        # setup QtWidget to cover whole desktop
        screen_width = ctypes.windll.user32.GetSystemMetrics(78)
        screen_height = ctypes.windll.user32.GetSystemMetrics(79)
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.setWindowOpacity(0.3)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

        # set class for start/end point
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        
        self.show()

    def paintEvent(self, event):
        rect = QtGui.QPainter(self)
        rect.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 128), 2))
        rect.setBrush(QtGui.QColor(128, 128, 128, 128))
        rect.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()

        # find top right and bottom left
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        # save copy of screen and call upload
        saveRectToBmp('capture.bmp', rect=(x1, y1, x2, y2))
        Image.open('capture.bmp').save('capture.png')
        upload('capture.png')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    snippingTool = SnipWindow()
    snippingTool.show()
    
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())
