#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import Frame, Label, Button

class ImageBox(Frame):
    def __init__(self, parent, controller, image):
        Frame.__init__(self,parent)

        self.__controller = controller
        self.__image = image

        self.__lock = False
        self.__selected = False

        self.__buttonRemove = None

        self.__initLayout()
        
    def __initLayout(self):
        '''__initProjectLayout()
            Projekt ablak
        '''
        ### Beállítások ###
        self.config(width=150, height=150, bg="light cyan")

        self.pack_propagate(False)

        image = self.__image.getImageTk((140, 140))

        ### Elemek létrehozása ###
        labelImage = Label(self, image=image)
        self.__buttonRemove = Button(self, text="X", command=self.onRemove)
        
        labelImage.image = image
        
        ### Elhelyezés ###
        labelImage.pack(padx=5, pady=5)
        self.__buttonRemove.place(x=130, y=0)

        ### Eventek ###
        labelImage.bind("<Button-1>", self.onSelect)

    def lockControl(self, lock=True):
        try:
            if lock:
                self.__lock = True
                self.__buttonRemove['state'] = 'normal'
            else:
                self.__lock = False
                self.__buttonRemove['state'] = 'normal'
        except AttributeError:
            pass
        except TypeError:
            pass

    def isSelected(self):
        return self.__selected
    
    def onSelect(self, *_):
        if self.__lock:
            return

        if self.__selected:
            self.__selected = False
            self.config(bg="light cyan")

            self.__controller.selectImage(False)
        else:
            if self.__controller.selectImage(True):
                self.__selected = True
                self.config(bg="dark sea green")

    def onRemove(self):
        self.__controller.removeImage(self)
    
    def getImagePath(self):
        return self.__image.getImagePath()

    def getImage(self):
        return self.__image
