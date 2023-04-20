#імпортуєм не обхідні бібліотеки
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image, ImageFilter
from PyQt5.QtCore import Qt

from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
)

def pil2pixmap(im):
    if im.mode == "RGB":
        r, g, b = im.split()
        im = Image.merge("RGB", (b, g, r))
    elif  im.mode == "RGBA":
        r, g, b, a = im.split()
        im = Image.merge("RGBA", (b, g, r, a))
    elif im.mode == "L":
        im = im.convert("RGBA")
    im2 = im.convert("RGBA")
    data = im2.tobytes("raw", "RGBA")
    qim = QImage(data, im.size[0], im.size[1], QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(qim)
    return pixmap

folderName = ""

#створюєм віджет вікна
app = QApplication([])
win = QWidget()
win.setWindowTitle("недо фото едітор 2077")
win.resize(1000, 800)

app.setStyleSheet("""
        QWidget {
            background: #242424;
        }
        QPushButton {
            background: #606060;
            color: #FFFFFF;
            min-height: 50px;
            min-width: 110px;
            border-radius: 5px;
            margin: 0px;
        }
        QGroupBox {
            background: #242424;
            min-height: 100px;
            min-width: 600px;           
            border-radius: 5px;
            margin: 0px;
        }
        QLabel {
            color: #B7B7B7;
            font-size: 25px;
        }
        QListWidget {
            border-style: hidden;
            color: #B7B7B7;
        }
        """)

#створюєм кнопки
btnFolder = QPushButton("Папка")
btnBlur = QPushButton("Розмиття")
btnLeft = QPushButton("Ліворуч")
btnRight = QPushButton("Праворуч")
btnFind_Edges = QPushButton("Знайти края")
btnContour = QPushButton("Контур")
btnMirror = QPushButton("Дзеркало")
btnSave = QPushButton("Зберегти")
btnSharpness = QPushButton("Різкість")
btnEmboss = QPushButton("Тисненя")
btnBlackWhite = QPushButton("Ч/Б")
photoLabel = QLabel(" ")
photoList = QListWidget()

#створюєм колонки
mainLine = QHBoxLayout()
leftColumn = QVBoxLayout()
rightColumn = QVBoxLayout()

#додаєм до лівої колонки об'єкти
leftColumn.addWidget(btnFolder)
leftColumn.addWidget(btnSave)
leftColumn.addWidget(photoList)
mainLine.addLayout(leftColumn)

#додаєм до правої колонки об'єкти
rightColumn.addWidget(photoLabel, alignment=Qt.AlignCenter)
horizontalLine = QHBoxLayout()
horizontalLine.addWidget(btnLeft)
horizontalLine.addWidget(btnEmboss)
horizontalLine.addWidget(btnRight)
horizontalLine.addWidget(btnMirror)
horizontalLine.addWidget(btnSharpness)
horizontalLine.addWidget(btnContour)
horizontalLine.addWidget(btnBlackWhite)
horizontalLine.addWidget(btnFind_Edges)
horizontalLine.addWidget(btnBlur)
rightColumn.addLayout(horizontalLine)
mainLine.addLayout(rightColumn)

win.setLayout(mainLine)

dialog = QFileDialog(parent=win)

def chooseWorkFolder():
    global folderName
    folderName = QFileDialog.getExistingDirectory()

def showFileNames():
    fileExtension = ["jpg", "png", "jpeg"]

    chooseWorkFolder()
    files = os.listdir(folderName)
    newFile = []
    for file in files:
        ext = file.split(".")
        if len(ext) >= 2:
            ext = ext[1]
            if ext in fileExtension:
                newFile.append(file)

    photoList.clear()
    photoList.addItems(newFile)


class ImageEditor:
    def __init__(self):
        self.image = None
        self.folder = None
        self.filename = None

    def loadImage(self):
        imagePath = os.path.join(self.folder, self.filename)
        self.image = Image.open(imagePath)

    def showImage(self):
        pixel = pil2pixmap(self.image)
        pixel = pixel.scaled(550, 550, Qt.KeepAspectRatio)
        photoLabel.setPixmap(pixel)

    def doBlackWhite(self):
        self.image = self.image.convert("L")
        self.showImage()

    def doEmboss(self):
        self.image = self.image.filter(EMBOSS)
        self.showImage()

    def doContour(self):
        self.image = self.image.filter(CONTOUR)
        self.showImage()

    def doSharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.showImage()

    def doLeft(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.showImage()

    def doRight(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.showImage()

    def doMirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.showImage()

    def doBlur(self):
        self.image = self.image.filter(BLUR)
        self.showImage()

    def doFind_Edges(self):
        self.image = self.image.filter(FIND_EDGES)
        self.showImage()

    def saveImage(self):
        filename, _ = QFileDialog.getSaveFileName(None, 'Save Image', '',
                                                  'Images (*.png *.jpg);;All Files (*)')
        if filename:
            self.image.save(filename)


imageEditor = ImageEditor()

def showChosenImage():
    imageEditor.folder = folderName
    imageEditor.filename = photoList.currentItem().text()
    imageEditor.loadImage()
    imageEditor.showImage()


btnFolder.clicked.connect(showFileNames)
btnSave.clicked.connect(imageEditor.saveImage)
btnEmboss.clicked.connect(imageEditor.doEmboss)
btnFind_Edges.clicked.connect(imageEditor.doFind_Edges)
btnLeft.clicked.connect(imageEditor.doLeft)
btnBlur.clicked.connect(imageEditor.doBlur)
btnRight.clicked.connect(imageEditor.doRight)
btnBlackWhite.clicked.connect(imageEditor.doBlackWhite)
btnMirror.clicked.connect(imageEditor.doMirror)
btnContour.clicked.connect(imageEditor.doContour)
btnSharpness.clicked.connect(imageEditor.doSharpen)
photoList.currentRowChanged.connect(showChosenImage)
win.show()
app.exec_()