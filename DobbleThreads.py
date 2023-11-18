#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import time

from ImP import ImP
from DobbleImage import DobbleImage

class ImageLoadingThread(threading.Thread):
    def __init__(self, master, imagesPath):
        threading.Thread.__init__(self)

        self.__master = master
        self.__imagesPath = imagesPath

    def run(self):
        for imagePath in self.__imagesPath:
            self.__master.setStatusText("Kép betöltése: %s" % imagePath)
            image = ImP(imagePath)
            self.__master.addImageToProject(image)
            self.__master.updateProgressBar(1)
        self.__master.setStatusText("")
        self.__master.updateProgressBar(0)

        self.__master.openImageDone()

class GenerateCardThread(threading.Thread):
    def __init__(self, master, images, cardId = None):
        threading.Thread.__init__(self)

        self.__master = master
        self.__images = images
        self.__cardId = cardId
        self.__startTime = 0
        self.__iSum = 0

    def __getRemainingTime(self, counter):
        fullTime = ((time.time() - self.__startTime) / counter) * (self.__iSum - counter)
        fullSec = int(fullTime) % 60
        fullMin = int(fullTime / 60)

        return "%s perc, %s másodperc" % (fullMin, fullSec)

    def run(self):
        self.__startTime = time.time()

        iNum = self.__master.getCardMaster().getImagesNum()
        ipC = self.__master.getCardMaster().getImagesPerCard()

        self.__iSum = ipC

        counter = 1
        trying = 0

        if self.__cardId is None:
            self.__master.getCardMaster().clearCards()

            self.__iSum *= iNum

            i = 0

            while i != self.__master.getCardMaster().getImagesNum():
                card = self.__master.getCardMaster().addCard(DobbleImage(ipC))

                for j in range(ipC):
                    image = card.addImage(self.__images[i][j])

                    if image == -1:
                        if trying == 5:
                            self.__master.generateError()
                            return

                        self.__master.getCardMaster().removeCard(-1)
                        i -= 1
                        trying += 1
                        break
                    else:
                        trying = 0

                    self.__master.setStatusText("Generálás... Befejezés: %s" % self.__getRemainingTime(counter))
                    self.__master.updateProgressBar(1)
                    counter += 1

                i += 1
        else:
            card = DobbleImage(ipC)

            done = False

            while not done:
                for j in range(ipC):
                    image = card.addImage(self.__images[j])
                    if image == -1:
                        if trying == 5:
                            self.__master.generateError()
                            return

                        card = DobbleImage(ipC)
                        trying += 1
                        done = False
                        break

                    self.__master.setStatusText("Generálás... Befejezés: %s" % self.__getRemainingTime(counter))
                    self.__master.updateProgressBar(1)
                    counter += 1

                    self.__master.getCardMaster().setCard(self.__cardId, card)
                    done = True


        self.__master.setStatusText("")
        self.__master.updateProgressBar(0)
        self.__master.generateDone()

class GeneratePdfThread(threading.Thread):
    def __init__(self, master):
        threading.Thread.__init__(self)

        self.__master = master
        self.__iNum = self.__master.getCardMaster().getImagesNum()
        self.__startTime = 0

    def __getRemainingTime(self, counter):
        fullTime = ((time.time() - self.__startTime) / counter) * (self.__iNum - counter)
        fullSec = int(fullTime) % 60
        fullMin = int(fullTime / 60)

        return "%s perc, %s másodperc" % (fullMin, fullSec)

    def run(self):
        self.__startTime = time.time()

        counter = 1

        self.__master.setStatusText("Exportálás...")

        while self.__master.getCardMaster().addImageToPdf():
            self.__master.setStatusText("Exportálás... Befejezés: %s" % self.__getRemainingTime(counter))
            self.__master.updateProgressBar(1)

            counter += 1

        self.__master.setStatusText("")
        self.__master.updateProgressBar(0)
        self.__master.exportDone()