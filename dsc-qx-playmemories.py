#!/usr/bin/env python3
#
# @@file:dsc-playmemories.py
# @@description: live stream Sony DSC-QX Lens-Style to desktop
# @@version: 1.0
# @@author: Loouis Low <loouis@gmail.com>
#

import sys
import json
import time
import http.client
import urllib.parse
import threading
import base64
import hashlib
import functools

from PyQt4.QtCore import *
from PyQt4.QtGui import *

# prerequisites
try:
    import PyQt4
except:
    os.system("pip install -r requirements.txt")
    os.system("sudo bash prerequisites.sh")

lock = threading.Lock()

app = QApplication(sys.argv)
image = QImage()
overviewgrid = "off"


class ImageDisplay(QLabel):

    def __init__(self):

        QLabel.__init__(self)

    def paintEvent(self, event):

        global lock
        global overviewgrid

        lock.acquire()

        try:
            # draws bullseye cross on image
            if overviewgrid == "bullseye":
                qp = QPainter()
                image_height = image.height()
                image_width = image.width()
                bull_size = 150

                qp.begin(image)
                pen = QPen(Qt.red, 1, Qt.SolidLine)
                qp.setPen(pen)
                qp.drawLine(image_width / 2, bull_size, image_width / 2, image_height - bull_size)
                qp.drawLine((bull_size * 1.5), image_height / 2, image_width - (bull_size * 1.5), image_height / 2)
                qp.end()
                self.setPixmap(QPixmap.fromImage(image))
            # draws gridlines on image
            elif overviewgrid == "gridlines":
                qp = QPainter()
                image_height = image.height()
                image_width = image.width()

                qp.begin(image)
                pen = QPen(Qt.white, 1, Qt.SolidLine)
                qp.setPen(pen)
                grid_h = image_width / 20;
                grid_v = image_height / 15;
                for n in range(0, 20):
                    qp.drawLine(grid_h * n, 0, grid_h * n, image_height)
                for n in range(0, 15):
                    qp.drawLine(0, grid_v * n, image_width, grid_v * n)

                qp.end()

                self.setPixmap(QPixmap.fromImage(image))
            else:
                self.setPixmap(QPixmap.fromImage(image))

        finally:
            lock.release()

        QLabel.paintEvent(self, event)


# params based on DSC-QX API
pId = 0
headers = {"Content-type": "text/plain", "Accept": "*/*", "X-Requested-With": "com.sony.playmemories.mobile"}
AUTH_CONST_STRING = "90adc8515a40558968fe8318b5b023fdd48d3828a2dda8905f3b93a3cd8e58dc"
METHODS_TO_ENABLE = "camera/setFlashMode:camera/getFlashMode:camera/getSupportedFlashMode:camera/getAvailableFlashMode:camera/setExposureCompensation:camera/getExposureCompensation:camera/getSupportedExposureCompensation:camera/getAvailableExposureCompensation:camera/setSteadyMode:camera/getSteadyMode:camera/getSupportedSteadyMode:camera/getAvailableSteadyMode:camera/setViewAngle:camera/getViewAngle:camera/getSupportedViewAngle:camera/getAvailableViewAngle:camera/setMovieQuality:camera/getMovieQuality:camera/getSupportedMovieQuality:camera/getAvailableMovieQuality:camera/setFocusMode:camera/getFocusMode:camera/getSupportedFocusMode:camera/getAvailableFocusMode:camera/setStillSize:camera/getStillSize:camera/getSupportedStillSize:camera/getAvailableStillSize:camera/setBeepMode:camera/getBeepMode:camera/getSupportedBeepMode:camera/getAvailableBeepMode:camera/setCameraFunction:camera/getCameraFunction:camera/getSupportedCameraFunction:camera/getAvailableCameraFunction:camera/setLiveviewSize:camera/getLiveviewSize:camera/getSupportedLiveviewSize:camera/getAvailableLiveviewSize:camera/setTouchAFPosition:camera/getTouchAFPosition:camera/cancelTouchAFPosition:camera/setFNumber:camera/getFNumber:camera/getSupportedFNumber:camera/getAvailableFNumber:camera/setShutterSpeed:camera/getShutterSpeed:camera/getSupportedShutterSpeed:camera/getAvailableShutterSpeed:camera/setIsoSpeedRate:camera/getIsoSpeedRate:camera/getSupportedIsoSpeedRate:camera/getAvailableIsoSpeedRate:camera/setExposureMode:camera/getExposureMode:camera/getSupportedExposureMode:camera/getAvailableExposureMode:camera/setWhiteBalance:camera/getWhiteBalance:camera/getSupportedWhiteBalance:camera/getAvailableWhiteBalance:camera/setProgramShift:camera/getSupportedProgramShift:camera/getStorageInformation:camera/startLiveviewWithSize:camera/startIntervalStillRec:camera/stopIntervalStillRec:camera/actFormatStorage:system/setCurrentTime"


def postRequest(conn, target, req):
    global pId
    pId += 1
    req["id"] = pId

    conn.request("POST", "/sony/" + target, json.dumps(req), headers)
    response = conn.getresponse()
    data = json.loads(response.read().decode("UTF-8"))

    # print(data)
    if data["id"] != pId:
        return {}

    return data


def exitWithError(conn, message):
    conn.close()
    sys.exit(1)


def parseUrl(url):
    parsedUrl = urllib.parse.urlparse(url)
    return parsedUrl.hostname, parsedUrl.port, parsedUrl.path + "?" + parsedUrl.query, parsedUrl.path[1:]


# download image from the device
def downloadImage(url):
    host, port, address, img_name = parseUrl(url)
    conn2 = http.client.HTTPConnection(host, port)
    conn2.request("GET", address)
    response = conn2.getresponse()

    if response.status == 200:
        with open(img_name, "wb") as img:
            img.write(response.read())
            print("[debug] Saving picture to computer")
    else:
        print("ERROR: Could not download picture, error = [%d %s]" % (response.status, response.reason))


# get liveview from the device
def liveviewFromUrl(url):
    global image
    global lock

    host, port, address, img_name = parseUrl(url)
    conn3 = http.client.HTTPConnection(host, port)
    conn3.request("GET", address)
    response = conn3.getresponse()

    if response.status == 200:
        buf = b''
        c = 0
        while not response.closed:
            nextPart = response.read(1024)
            jpegStart = nextPart.find(b'\xFF\xD8\xFF')
            jpegEnd = nextPart.find(b'\xFF\xD9')
            if jpegEnd != -1:
                c += 1
                buf += nextPart[:jpegEnd + 2]
                lock.acquire()
                try:
                    image.loadFromData(buf)
                finally:
                    lock.release()
            if jpegStart != -1:
                buf = nextPart[jpegStart:]
            else:
                buf += nextPart


def communicationThread():
    conn = http.client.HTTPConnection("10.0.0.1", 10000)
    resp = postRequest(conn, "camera", {"method": "getVersions", "params": []})
    resp = postRequest(conn, "camera", {"method": "getVersions", "params": []})

    if resp["result"][0][0] != "1.0":
        exitWithError(conn, "Unsupported version")

    resp = postRequest(conn, "accessControl", {"method": "actEnableMethods", "params": [
        {"methods": "", "developerName": "", "developerID": "", "sg": ""}], "version": "1.0"})
    dg = resp["result"][0]["dg"]

    h = hashlib.sha256()
    h.update(bytes(AUTH_CONST_STRING + dg, "UTF-8"))
    sg = base64.b64encode(h.digest()).decode("UTF-8")

    resp = postRequest(conn, "camera", {"method": "startLiveview", "params": [], "version": "1.0"})

    liveview = threading.Thread(target=liveviewFromUrl, args=(resp["result"][0],))
    liveview.start()


# draw form UI
class Form(QDialog):

    def __init__(self, parent=None):

        super(Form, self).__init__(parent)

        # camera functions
        takePicBtn = QPushButton("Take Picture")
        self.label = QLabel("Standing by..")

        # live stream
        imgDisplay = ImageDisplay()
        imgDisplay.setMinimumSize(640, 480)
        imgDisplay.show()

        grid = QGridLayout()
        grid.addWidget(imgDisplay, 1, 0)

        controlLayout = QGridLayout()
        controlLayout.setSpacing(10)
        controlLayout.addWidget(takePicBtn, 0, 0)

        self.getSupportedExposureModes(grid)
        grid.addLayout(controlLayout, 2, 0)

        self.setLayout(grid)

        self.connect(takePicBtn, SIGNAL("clicked()"), self.takePic)

    def getSupportedExposureModes(self, grid):

        conn = http.client.HTTPConnection("10.0.0.1", 10000)
        resp = postRequest(conn, "camera", {"method": "getAvailableExposureMode", "params": [], "version": "1.0"})
        self.label.setText("Current Mode:" + resp["result"][0])
        available_modes = resp["result"][1]

        layout = QHBoxLayout()
        label = QLabel("Camera Modes:")
        layout.addWidget(label)

        for m in available_modes:
            b = QPushButton(m)
            self.connect(b, SIGNAL("clicked()"), functools.partial(self.setExposureMode, m, grid))
            layout.addWidget(b)
        layout.addStretch()
        grid.addLayout(layout, 0, 0)

    def setExposureMode(self, m, grid):

        self.label.setText("Setting Mode")
        conn = http.client.HTTPConnection("10.0.0.1", 10000)
        resp = postRequest(conn, "camera", {"method": "setExposureMode", "params": [m], "version": "1.0"})

        if resp["result"][0] == 0:
            self.clearCombo(self.ISOComboBox)
            self.clearCombo(self.FComboBox)
            self.clearCombo(self.ShutterComboBox)

            self.label.setText("New Mode Set:" + m)
            self.getAvailableFNumber(grid)
            self.getAvailableIsoSpeedRate(grid)
            self.getAvailableShutterSpeed(grid)

    def getAvailableFNumber(self, grid):

        conn = http.client.HTTPConnection("10.0.0.1", 10000)
        resp = postRequest(conn, "camera", {"method": "getAvailableFNumber", "params": [], "version": "1.0"})

        try:
            available_modes = resp["result"][1]
            self.FComboBox.addItems(available_modes)

        except:
            pass

    def getAvailableIsoSpeedRate(self, grid):

        conn = http.client.HTTPConnection("10.0.0.1", 10000)
        resp = postRequest(conn, "camera", {"method": "getAvailableIsoSpeedRate", "params": [], "version": "1.0"})
        try:
            available_modes = resp["result"][1]
            self.ISOComboBox.addItems(available_modes)

        except:
            pass

    def getAvailableShutterSpeed(self, grid):

        conn = http.client.HTTPConnection("10.0.0.1", 10000)
        resp = postRequest(conn, "camera", {"method": "getAvailableShutterSpeed", "params": [], "version": "1.0"})
        try:
            available_modes = resp["result"][1]
            self.ShutterComboBox.addItems(available_modes)

        except:
            pass

    def takePic(self):

        self.label.setText("Capturing Image")
        conn = http.client.HTTPConnection("10.0.0.1", 10000)
        resp = postRequest(conn, "camera", {"method": "actTakePicture", "params": [], "version": "1.0"})
        downloadImage(resp["result"][0][0])

    def zoomIn(self):

        self.label.setText("Zoom In")
        conn = http.client.HTTPConnection("10.0.0.1", 10000)
        resp = postRequest(conn, "camera", {"method": "actZoom", "params": ["in", "start"], "version": "1.0"})

    def zoomInStop(self):

        conn = http.client.HTTPConnection("10.0.0.1", 10000)
        resp = postRequest(conn, "camera", {"method": "actZoom", "params": ["in", "stop"], "version": "1.0"})
        feedback = postRequest(conn, "camera", {"method": "getEvent", "params": [False], "id": 4, "version": "1.0"})
        print(feedback["result"][2]["zoomPosition"])
        self.label.setText("Zoom Position: " + str(feedback["result"][2]["zoomPosition"]))

    def zoomOut(self):

        self.label.setText("Zoom In")
        conn = http.client.HTTPConnection("10.0.0.1", 10000)
        resp = postRequest(conn, "camera", {"method": "actZoom", "params": ["out", "start"], "version": "1.0"})

    def zoomOutStop(self):

        conn = http.client.HTTPConnection("10.0.0.1", 10000)
        resp = postRequest(conn, "camera", {"method": "actZoom", "params": ["out", "stop"], "version": "1.0"})
        feedback = postRequest(conn, "camera", {"method": "getEvent", "params": [False], "id": 4, "version": "1.0"})
        print(feedback["result"][2]["zoomPosition"])
        self.label.setText("Zoom Position: " + str(feedback["result"][2]["zoomPosition"]))

    def handleFChange(self, text):

        print('handleChanged: %s' % text)
        conn = http.client.HTTPConnection("10.0.0.1", 10000)
        resp = postRequest(conn, "camera", {"method": "setFNumber", "params": [text], "version": "1.0"})

    def handleISOChange(self, text):

        print('handleChanged: %s' % text)
        conn = http.client.HTTPConnection("10.0.0.1", 10000)
        resp = postRequest(conn, "camera", {"method": "setIsoSpeedRate", "params": [text], "version": "1.0"})

    def handleShutterChange(self, text):

        print('handleChanged: %s' % text)
        conn = http.client.HTTPConnection("10.0.0.1", 10000)
        resp = postRequest(conn, "camera", {"method": "setShutterSpeed", "params": [text], "version": "1.0"})

    def clearCombo(self, combo):

        for i in range(combo.count(), -1, -1):
            print(i)
            combo.removeItem(i)


form = Form()
form.show()

if __name__ == "__main__":
    communication = threading.Thread(target=communicationThread)
    communication.start()
    sys.exit(app.exec_())
