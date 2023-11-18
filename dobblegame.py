#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------
 Name:        dobblegame.py
 Author:      Tibor Varga

 Created:     28-01-2020
---------------------------------------------------------------------------
"""
import tkinter as tk
from tkview.MainFrame import MainFrame

VERSION = "0.9.0"

root = tk.Tk()
#root.iconbitmap(".\\icon.ico")
app = MainFrame(root)
root.mainloop()
