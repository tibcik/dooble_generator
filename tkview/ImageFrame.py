#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkview.ImageBox import ImageBox

from tkinter import Frame, Button, Label, Scrollbar, Canvas, messagebox
from tkinter import VERTICAL, LEFT, RIGHT, BOTH, Y, X, N, DISABLED, NORMAL, NW

class ImageFrame(Frame):
    def __init__(self, parent, controller, imagesNum):
        Frame.__init__(self, parent)

        self.__controller = controller
        self.__imagesNum = imagesNum

        self.__imagesBox = {}            # {tkview.ImageBox}
        self.__maxColumn = 4             # tkview.Integer
        self.__backImage = None          # ImageBox
        self.__selectedImages = 0        # Integer

        self.__buttonGenerate = None     # tkinter.Buttom
        self.__buttonSelectAll = None    # tkinter.Button
        self.__labelInfo = None          # tkinter.Label
        self.__canvas = None             # tkinter.Canvas
        self.__interior = None           # tkinter.Frame
        self.__interiorId = 0            # Integer

        self.__resizable = True

        self.__initLayout()

    def __initLayout(self):
        '''__initProjectLayout()
            Projekt ablak
        '''
        ### Beállítások ###

        ### Elemek létrehozása ###
        box1 = Frame(self)
        box2 = Frame(self)

        self.__buttonGenerate = Button(box1, text="Generálás", command=self.onGenerate)
        self.__buttonSelectAll = Button(box1, text="Mind kijelölése", command=self.onSelectAll)
        self.__labelInfo = Label(box1, text="Jelöljön ki %s képet. Még %s kép van hátra." % (self.__imagesNum, self.__imagesNum))

        vscroll = Scrollbar(box2, orient=VERTICAL)
        self.__canvas = Canvas(box2, yscrollcommand=vscroll.set)
        self.__interior = Frame(self.__canvas)

        # Beállítások
        vscroll.config(command=self.__canvas.yview)
        self.__canvas.xview_moveto(0)
        self.__canvas.yview_moveto(0)
        self.__interiorId = self.__canvas.create_window(0, 0, window=self.__interior, anchor=NW)
        
        ### Elhelyezés ###
        self.__buttonGenerate.pack(padx=20, pady=10, side=LEFT)
        self.__labelInfo.pack(side=LEFT, expand=True)
        self.__buttonSelectAll.pack(padx=20, pady=10, side=RIGHT)

        vscroll.pack(fill=Y, side=RIGHT, expand=False)
        self.__canvas.pack(fill=BOTH, anchor=N, expand=True)

        box1.pack(fill=X)
        box2.pack(fill=BOTH, expand=True)

        ### Eventek ###
        self.__interior.bind('<Configure>', self.onConfigureInterior)
        self.__canvas.bind('<Configure>', self.onConfigureCanvas)
        self.bind("<Configure>", self.onResize)

    def lockControl(self, lock=True):
        try:
            if lock:
                self.__buttonGenerate['state'] = DISABLED
                self.__buttonSelectAll['state'] = DISABLED
                for iBox in self.__imagesBox:
                    iBox.lockControl()
            else:
                self.__buttonGenerate['state'] = NORMAL
                self.__buttonSelectAll['state'] = NORMAL
                for iBox in self.__imagesBox:
                    iBox.lockControl(False)
        except AttributeError:
            pass
        except TypeError:
            pass

    def onConfigureInterior(self, *_):
        size = (self.__interior.winfo_reqwidth(), self.__interior.winfo_reqheight())
        self.__canvas.config(scrollregion="0 0 %s %s" % size)
        if self.__interior.winfo_reqwidth() != self.__canvas.winfo_width():
            self.__canvas.config(width=self.__interior.winfo_reqwidth())
        
    def onConfigureCanvas(self, *_):
        if self.__interior.winfo_reqwidth() != self.__canvas.winfo_width():
            # update the inner frame's width to fill the canvas
            self.__canvas.itemconfigure(self.__interiorId, width=self.__canvas.winfo_width())

    def onResize(self, event):
        if not self.__resizable:
            return
        self.__maxColumn = (int)((event.width - 16) / 150)
        self.__rebuildGrid()

    def onSelectAll(self):
        for iBox in self.__imagesBox:
            if not iBox.isSelected():
                if self.__imagesNum > self.__selectedImages:
                    iBox.onSelect(None)
    
    def onGenerate(self):
        if self.__imagesNum > self.__selectedImages:
            messagebox.showerror("Hiba", message="Nem választott ki elég képet!")
        elif self.__imagesNum < self.__selectedImages:
            messagebox.showerror("Hiba", message="Túl sok képet választott ki!")
        else:
            self.__controller.generateCards()

    def getSelectedImages(self, num):
        i = 0

        for iBox in self.__imagesBox:
            if iBox.isSelected():
                if i == num:
                    return iBox.getImage()
                i += 1

        return None

    def addImage(self, image):
        for iBox in self.__imagesBox:
            if iBox.getImagePath() == image.getImagePath():
                return False
        
        imageBox = ImageBox(self.__interior, self, image)

        self.__imagesBox[imageBox] = imageBox

        self.__rebuildGrid()

    def addBackImage(self, image):
        if self.__backImage is not None:
            messagebox.showerror("Hiba", message="Előszőr törölje az előző háttérképet!")
            return False
        
        imageBox = ImageBox(self.__interior, self, image)

        self.__backImage = imageBox

        self.__rebuildGrid()

    def updateInfoText(self):
        self.__labelInfo['text'] = "Jelöljön ki %s képet. Még %s kép van hátra." % (self.__imagesNum, self.__imagesNum - self.__selectedImages)

    def selectImage(self, select):
        if select:
            if self.__imagesNum <= self.__selectedImages:
                return False

            self.__selectedImages += 1
        else:
            self.__selectedImages -= 1

        self.updateInfoText()
        return True

    def removeImage(self, iBox):
        if iBox.isSelected():
            self.selectImage(False)

        self.__imagesBox[iBox].destroy()
        self.__imagesBox.pop(iBox)

        self.__rebuildGrid()

    def lockResize(self, lock):
        if lock:
            self.__resizable = False
        else:
            self.__resizable = True
    
    def __rebuildGrid(self):
        row = 1
        column = 0

        for iBox in self.__imagesBox:
            iBox.grid(row=row, column=column)

            column += 1
            if column == self.__maxColumn:
                #if row == 1 or (self.__width < 250 and row == 2):
                #    self.interior.placer.grid(row=1, column=column, padx=int((self.__width - self.__maxColumn * 150) / 2) - 2)

                column = 0
                row += 1

        if self.__backImage is not None:
            self.__backImage.grid(row=row, column=column)