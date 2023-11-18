#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
PDF Készítés
'''

from io import BytesIO
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A3
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

class DobblePdf:
    def __init__(self):
        self.__pageSize = A4
        self.__row = 0
        self.__column = 0
        self.__cardSize = 0
        self.__pdf = None
        self.__page = None

        self.__drawSize = (int(self.__pageSize[0] / mm) - 10, int(self.__pageSize[1] / mm) - 10)

    def setCardSize(self, cardSize):
        try:
            int(cardSize)
        except ValueError:
            print("DobblePdf->setCardSize(cardSize): Csak egész érték lehet! A jelenlegi érték marad: {}".format(self.__cardSize))
            return

        self.__cardSize = cardSize

    def addImage(self, img):
        if self.__pdf is None:
            self.__pdf = PdfFileWriter()
            self.__page = self.__pdf.addBlankPage(width=self.__pageSize[0], height=self.__pageSize[1])

        if (self.__column + 1) * self.__cardSize > self.__drawSize[0]:
            self.__row += 1
            self.__column = 0
        
        if (self.__row + 1) * self.__cardSize > self.__drawSize[1]:
            self.__page = self.__pdf.addBlankPage(width=self.__pageSize[0], height=self.__pageSize[1])
            self.__row = 0
                    
        imgTemp = BytesIO()
        imgDoc = canvas.Canvas(imgTemp, pagesize=A3)

        tmpImg = ImageReader(img)

        imgDoc.drawImage(tmpImg,
                        (10 + self.__column * self.__cardSize) * mm,
                        (self.__drawSize[1] - ((self.__row + 1) * self.__cardSize)) * mm,
                        width=self.__cardSize*mm, height=self.__cardSize*mm)
        imgDoc.save()
        self.__page.mergePage(PdfFileReader(BytesIO(imgTemp.getvalue())).getPage(0))

        self.__column += 1

    def savePdf(self, file):
        self.__pdf.write(file)