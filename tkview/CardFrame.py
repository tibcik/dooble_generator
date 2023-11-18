#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import Frame, Button, Label

class CardFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.__controller = controller

        self.__selectedCard = 0
        self.__initialized = False

        self.__buttonPrevCard = None
        self.__buttonRegenerate = None
        self.__buttonNextCard = None
        self.__labelInfo = None
        self.__labelImage = None
        
        self.config(width=0)

        #self.__initLayout()

    def initLayout(self):
        '''__initProjectLayout()
            Projekt ablak
        '''
        ### Beállítások ###
        self.grid_columnconfigure(0, minsize=100)
        self.grid_columnconfigure(1, minsize=100)
        self.grid_columnconfigure(2, minsize=100)

        self.grid_rowconfigure(0, pad=20)
        self.grid_rowconfigure(1, pad=10)
        self.grid_rowconfigure(2, minsize=300)
        self.grid_rowconfigure(3, pad=10)
        self.grid_rowconfigure(4, pad=10)
        self.grid_rowconfigure(5, pad=20)

        ### Elemek létrehozása ###
        # Elemek
        self.__buttonPrevCard = Button(self, text="<", command=self.onPrevCard, width=2)
        self.__buttonRegenerate = Button(self, text="Újragenerálás", command=self.onRegenerate, width=10)
        self.__buttonNextCard = Button(self, text=">", command=self.onNextCard, width=2)

        self.__labelInfo = Label(self, text="Kép: 0/0")
        self.__labelImage = Label(self)

        
        ### Elhelyezés ###
        self.__buttonPrevCard.grid(row=0, column=0, padx=10)
        self.__buttonRegenerate.grid(row=0, column=1)
        self.__buttonNextCard.grid(row=0, column=2, padx=10)
        self.__labelInfo.grid(row=1, column=0, columnspan=3)
        self.__labelImage.grid(row=2, column=0, columnspan=3)

        self.updateImage()

        self.__initialized = True

    def isInitialized(self):
        return self.__initialized

    def lockControl(self, lock = True):
        try:
            if lock:
                self.__buttonPrevCard['state'] = 'disabled'
                self.__buttonRegenerate['state'] = 'disabled'
                self.__buttonNextCard['state'] = 'disabled'
            else:
                self.__buttonPrevCard['state'] = 'normal'
                self.__buttonRegenerate['state'] = 'normal'
                self.__buttonNextCard['state'] = 'normal'
        except AttributeError:
            pass
        except TypeError:
            pass
        
    def __setPageNum(self):
        self.__labelInfo['text'] = "Kártya: %s/%s" % (self.__selectedCard + 1, self.__controller.getCardMaster().getImagesNum())
    
    def onPrevCard(self):
        if self.__selectedCard == 0:
            self.__selectedCard = self.__controller.getCardMaster().getImagesNum() - 1
        else:
            self.__selectedCard -= 1

        self.updateImage()
    
    def onNextCard(self):
        if self.__controller.getCardMaster().getImagesNum() == -1:
            return

        if self.__selectedCard == (self.__controller.getCardMaster().getImagesNum() - 1):
            self.__selectedCard = 0
        else:
            self.__selectedCard += 1

        self.updateImage()
    
    def onRegenerate(self):
        self.__controller.regenerateCard(self.__selectedCard)

    def updateImage(self):
        image = self.__controller.getCardMaster().getCardTk(self.__selectedCard)

        self.__labelImage = Label(self, image=image)
        self.__labelImage.image = image
        self.__labelImage.grid(row=2, column=0, columnspan=3)

        self.__setPageNum()
