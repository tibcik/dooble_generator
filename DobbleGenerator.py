#!/usr/bin/python
# -*- coding: utf-8 -*-

import random


class DobbleGenerator:
    def __init__(self):
        self.__valid = False
        self.__table = []
        self.__images = 0

    def calculate(self, imagesPerCard):
        self.__valid = False
        self.__table = []
        self.__images = 0

        try:
            int(imagesPerCard)
        except ValueError:
            print("DobbleGenerator->calculate(imagesPerCard): Csak egész érték lehet!")
            return

        if imagesPerCard not in [3,4,5,6,8,9]:
            print("DobbleGenerator->calculate(imagesPerCard): Az érték csak a következők egyike lehet: 3, 4, 5, 6, 8, 9!")
            return

        self.__table = []
        self.__valid = True

        n = imagesPerCard

        self.__images = (n - 1)**2 + n

        for i in range(n):  
            self.__table.append([0])
            for j in range(1, n):
                self.__table[i].append(i * (n - 1) + j)

        for i in range(n - 1):
            for j in range(n - 1):
                card = n + i * (n - 1) + j
                self.__table.append([i + 1])
                for k in range(1, n):
                    num = k * (n - 1) + 1 + ((j + (k - 1) * i) % (n - 1))
                    self.__table[card].append(num)

        for i in self.__table:
            random.shuffle(i)

        #self.debug(imagesPerCard)

        return 0

    def getImagesNum(self):
        return self.__images

    def isValid(self):
        return self.__valid

    def getTable(self):
        return self.__table

    def debug(self, imagesPerCard):
        print("Valid: {}".format(self.__valid))
        if self.__valid:
            print("ImagesPerPage: {}\nImages: {}".format(imagesPerCard, self.__images))
            for i in self.__table:
                print(i)
