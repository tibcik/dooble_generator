#!/usr/bin/python
# -*- coding: utf-8 -*-

from DobbleGenerator import DobbleGenerator
from DobblePdf import DobblePdf

class CardMaster():
    def __init__(self):
        self.__generator = DobbleGenerator()
        self.__pdf = DobblePdf()

        self.__images = []
        self.__cardSize = 0
        self.__imagesPerCard = 0
        self.__pdfSize = 0

    def validateImagesPerCard(self, imagesPerCard):
        self.__generator.calculate(imagesPerCard)

        if self.__generator.isValid():
            self.__imagesPerCard = imagesPerCard
            return True

        self.__imagesPerCard = 0
        return False

    def isGeneratorValid(self):
        return self.__generator.isValid()

    def getImagesNum(self):
        return self.__generator.getImagesNum()

    def getImagesPerCard(self):
        return self.__imagesPerCard

    def getCardTable(self):
        if self.__generator.isValid():
            return self.__generator.getTable()

        return None

    def setCardSize(self, cardSize):
        self.__pdf.setCardSize(cardSize)

        self.__cardSize = cardSize

    def addCard(self, card):
        self.__images.append(card)

        return self.__images[-1]

    def setCard(self, cardId, card):
        self.__images[cardId] = card

    def removeCard(self, cardId):
        try:
            self.__images.remove(cardId)
        except KeyError:
            print("Nincs ilyen kártya...")

    def clearCards(self):
        self.__images.clear()

    def getCardTk(self, cardId):
        return self.__images[cardId].getThumbnail().getImageTk((300, 300))

    def isGenerated(self):
        if self.__generator.getImagesNum() == len(self.__images):
            return True
        else:
            return False

    def addImageToPdf(self):
        if self.__pdfSize == self.__generator.getImagesNum():
            return False

        self.__pdf.addImage(self.__images[self.__pdfSize].getImage())

        self.__pdfSize += 1

        return True

    def savePdf(self, fileName):
        self.__pdf.savePdf(fileName)

    def clear(self):
        self.__pdf = None
        self.__pdf = DobblePdf()
        self.__pdf.setCardSize(self.__cardSize)
