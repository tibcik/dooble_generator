#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import Frame, Menu, Label, Entry, Button
from tkinter import BOTH, N, W, E, LEFT, RIGHT
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar

from CardMaster import CardMaster
from DobbleThreads import ImageLoadingThread, GenerateCardThread, GeneratePdfThread

from .CardFrame import CardFrame
from .ImageFrame import ImageFrame

class MainFrame(Frame):
    def __init__(self, root):
        '''__init__(root)
            root    -- tkinter.Tk
        '''
        Frame.__init__(self, root)
        root.title("Kártya generátor")

        self.__master = root
        self.__cardMaster = CardMaster()

        self.__exportFile = None
        self.__progressStep = 0

        self.__menubar = None

        self.__box = None
        self.__labelError = None
        self.__entryCardSize = None
        self.__entryImagesPerCard = None

        self.__box1 = None
        self.__box2 = None
        self.__labelStatus = None
        self.__progressBar = None
        self.__cardPanel = None
        self.__imagePanel = None

        self.__thread = None

        self.__initMenu()
        self.__initLayout()

        self.pack(fill=BOTH, expand=True, anchor=N)
        self.config(bg="blue")

    ### Layout beállítása ###
    def __initMenu(self):
        '''__initMenu()
        '''
        self.__menubar = Menu(self.__master)

        filemenu = Menu(self.__menubar, tearoff=0)
        filemenu.add_command(label="Új project", command=self.onNewProject)
        filemenu.add_separator()
        filemenu.add_command(label="Képek megnyitása", command=self.onOpenImages)
        filemenu.add_separator()
        filemenu.add_command(label="Exportálás(PDF)", command=self.onExport)
        filemenu.add_separator()
        filemenu.add_command(label="Kilépés", command=self.__master.quit)

        self.__menubar.add_cascade(label="Fájl", menu=filemenu)

        self.__master.config(menu=self.__menubar)

    def __initLayout(self):
        '''__initLayout()
            Új projekt ablak
        '''
        ### Beállítások ###
        self.__master.resizable(False, False)
        self.__master.minsize(0, 0)
        
        ### Elemek létrehozása ###
        # Befoglalo dobnoz
        self.__box = Frame(self)

        # Elemek
        label0 = Label(self.__box, text="Új projekt létrehozása")
        label1 = Label(self.__box, text="Kártyák mérete (mm)")
        label2 = Label(self.__box, text="Képek száma egy kártyán")
        self.__labelError = Label(self.__box, fg="red")
        self.__entryCardSize = Entry(self.__box, width=10)
        self.__entryImagesPerCard = Entry(self.__box, width=10)
        button1 = Button(self.__box, text="Projek létrehozása", command=self.onCreateProject)

        ### Elhelyezés ###
        label0.grid(row=0, column=0, columnspan=2, padx=5, pady=20)
        label1.grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.__entryCardSize.grid(row=1, column=1, padx=5, pady=5)
        label2.grid(row=2, column=0, sticky=W, padx=5, pady=5)
        self.__entryImagesPerCard.grid(row=2, column=1, padx=5, pady=5)
        self.__labelError.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        button1.grid(row=4, column=1, sticky=E, padx=5, pady=10)

        self.__box.pack()

        self.__entryCardSize.insert(0, "80")
        self.__entryImagesPerCard.insert(0, "3")

        self.lockControl()

    def __initProjectLayout(self):
        '''__initProjectLayout()
            Projekt ablak
        '''
        ### Beállítások ###
        self.__master.resizable(1, 1)
        self.__master.minsize(625, 450)

        ### Elemek létrehozása ###
        # Befoglalo doboz
        self.__box1 = Frame(self)
        self.__box2 = Frame(self)

        # Elemek
        self.__labelStatus = Label(self.__box1, text="Info")
        self.__progressBar = Progressbar(self.__box1, length=400, mode='determinate')

        self.__cardPanel = CardFrame(self.__box2, self)
        self.__imagePanel = ImageFrame(self.__box2, self, self.__cardMaster.getImagesNum())
        
        ### Elhelyezés ###
        self.__labelStatus.pack(side=LEFT)
        self.__progressBar.pack(side=RIGHT, fill=BOTH)

        self.__cardPanel.pack(side=LEFT, anchor=N)
        self.__imagePanel.pack(side=LEFT, expand=True, fill=BOTH, anchor=N)
        self.__box2.pack(fill=BOTH, expand=True, anchor=N)
        self.__box1.pack(fill=BOTH)

    def getCardMaster(self):
        return self.__cardMaster

    def lockControl(self, lock = True):
        try:
            if lock:
                self.__menubar.entryconfig("Fájl", state="disabled")
                self.__imagePanel.lockControl()
                self.__cardPanel.lockControl()
            else:
                self.__menubar.entryconfig("Fájl", state="normal")
                self.__imagePanel.lockControl(False)
                self.__cardPanel.lockControl(False)
        except AttributeError:
            pass

    ### Eventek ###
    def onNewProject(self):
        self.__labelStatus.destroy()
        self.__progressBar.destroy()
        self.__cardPanel.destroy()
        self.__imagePanel.destroy()

        self.__box1.destroy()
        self.__box2.destroy()

        del(self.__labelStatus)
        del(self.__progressBar)
        del(self.__cardPanel)
        del(self.__imagePanel)

        del(self.__box1)
        del(self.__box2)

        self.lockControl()
        self.__initLayout()

    def onCreateProject(self):
        '''onCreateProject()
            Új projekt beállítasian ellenőrzése
        '''
        cardSize = 0
        imagesPerCard = 0

        try:
            cardSize = int(self.__entryCardSize.get())
        except ValueError:
            self.__labelError['text'] = "A kártya mérete csak egész szám lehet!"
            return

        try:
            imagesPerCard = int(self.__entryImagesPerCard.get())
        except ValueError:
            self.__labelError['text'] = "A kártyán lévő képek száma csak egész lehet."
            return

        if cardSize < 40 or cardSize > 190:
            self.__labelError['text'] = "A kértya mérete nem lehet kisebb mint\n40 mm és nem lehet nagyobb mint 190 mm."
            return

        if not self.__cardMaster.validateImagesPerCard(imagesPerCard):
            self.__labelError['text'] = "A kártyán lévő képek száma a\nkövetkezők egyike lehet: 3, 4, 5, 6, 8, 9."
            return

        self.__cardMaster.setCardSize(cardSize)

        ##########
        self.__labelError.destroy()
        self.__entryCardSize.destroy()
        self.__entryImagesPerCard.destroy()

        self.__box.destroy()

        del(self.__labelError)
        del(self.__entryCardSize)
        del(self.__entryImagesPerCard)
        del(self.__box)

        self.__initProjectLayout()
        self.lockControl(False)

    def onOpenImages(self):
        filetypes = (
            ("png", "*.png"),
            ("jpeg", "*.jpg")
        )
        files = filedialog.askopenfilenames(title = "Képek választása", filetypes=filetypes)
        
        if len(files) > 0:
            self.lockControl()

            self.updateProgressBar(0, len(files))
            self.__thread = ImageLoadingThread(self, files)
            self.__thread.start()

    def onExport(self):
        if not self.__cardMaster.isGenerated():
            messagebox.showerror("Hiba", "Előszőr generálja le a kártyákat!")
            return

        file = filedialog.asksaveasfile(mode='wb', filetypes=[('PDF', '.pdf')], defaultextension='.pdf')

        if file is None:
            return
        
        self.__exportFile = file

        self.lockControl()

        self.updateProgressBar(0, self.__cardMaster.getImagesNum())
        self.__thread = GeneratePdfThread(self)
        self.__thread.start()

    def openImageDone(self):
        del(self.__thread)
        self.lockControl(False)

    def exportDone(self):
        self.__cardMaster.savePdf(self.__exportFile)
        self.__exportFile.close()

        self.__cardMaster.clear()

        del(self.__thread)
        self.lockControl(False)

    def addImageToPanel(self, image):
        self.__imagePanel.addImage(image)

    def generateCards(self):
        dTable = self.__cardMaster.getCardTable()

        images = []

        for i in range(self.__cardMaster.getImagesNum()):
            images.append([])
            for j in range(self.__cardMaster.getImagesPerCard()):
                images[i].append(self.__imagePanel.getSelectedImages(dTable[i][j]))

        self.lockControl()

        self.updateProgressBar(0, self.__cardMaster.getImagesPerCard() * self.__cardMaster.getImagesNum())
        self.__thread = GenerateCardThread(self, images)
        self.__thread.start()

    def regenerateCard(self, cardId):
        dTable = self.__cardMaster.getCardTable()

        images = []

        for j in range(self.__cardMaster.getImagesPerCard()):
            images.append(self.__imagePanel.getSelectedImages(dTable[cardId][j]))

        self.lockControl()

        self.updateProgressBar(0, self.__cardMaster.getImagesPerCard())
        self.__thread = GenerateCardThread(self, images, cardId)
        self.__thread.start()

    def generateError(self):
        messagebox.showerror("Nem lehet a kártyákat legenerálni.\nLépjen kapcsolatba a fejlesztővel!")

    def generateDone(self):
        if self.__cardPanel.isInitialized():
            self.__cardPanel.updateImage()
        else:
            self.__imagePanel.lockResize(True)
            self.__cardPanel.initLayout()
            self.__imagePanel.lockResize(False)

        del(self.__thread)
        self.lockControl(False)

    def setStatusText(self, text):
        self.__labelStatus['text'] = text

    def updateProgressBar(self, pos, maxItem = 0):
        if maxItem > 0:
            try:
                self.__progressStep = 100 / maxItem
            except ValueError:
                print("MainFrame->updateProgressBar(step): Csak egész érték lehet!")
                return
            return

        if pos == 0:
            self.__progressBar['value'] = 0
        else:
            self.__progressBar['value'] += int(self.__progressStep * pos)

        self.__master.update_idletasks()

    def addImageToProject(self, image):
        try:
            self.__imagePanel.addImage(image)
        except AttributeError:
            print("Hiba!")