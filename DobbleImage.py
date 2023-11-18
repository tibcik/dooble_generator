#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------
 Name:        dobblegame.py
 Author:      Tibor Varga

 Created:     28-01-2020
---------------------------------------------------------------------------
"""

import random
import math

from ImP import ImP

from PIL import Image, ImageDraw
import numpy as np

class DobbleImage:
    def __init__(self, imagePerPage):
        self.__fullImageSize = 5000
        self.__thumbnailSize = 0
        self.__imagesPerPage = imagePerPage
        self.__thumbnail = None
        self.__images = []
        self.__modTable = []

        self.__placed = 0

    def getThumbnail(self):
        return ImP("", self.__thumbnail)

    def getImage(self):
        workSize = self.__fullImageSize

        fullImage = Image.new("RGBA", (workSize, workSize), color=(255, 255, 255, 0))
        draw = ImageDraw.Draw(fullImage)
        draw.ellipse([0, 0, workSize, workSize], width=1, outline=(0, 0, 0, 255))

        for i in range(len(self.__images)):
            if self.__imagesPerPage > 3 and i == 0:
                rotation = self.__modTable[0][0]
                work_image = self.__images[0].getCropImage().rotate(rotation, expand=True, resample=Image.BICUBIC)

                scale = self.__modTable[0][1]

                size = (
                    int(work_image.width * scale),
                    int(work_image.height * scale)
                )

                work_image = work_image.resize(size, resample=Image.LANCZOS)

                point = self.__modTable[0][2]

                placeImage = Image.new("RGBA", (workSize, workSize), color=(255, 255, 255, 0))
                placeImage.paste(work_image, point)
                fullImage = Image.alpha_composite(fullImage, placeImage)
            else:
                rotation = self.__modTable[i][0]
                work_image = self.__images[i].getCropImage().rotate(rotation, expand=True, resample=Image.BICUBIC)

                scale = self.__modTable[i][1]

                size = (
                    int(work_image.width * scale),
                    int(work_image.height * scale)
                )

                work_image = work_image.resize(size, resample=Image.LANCZOS)

                point = self.__modTable[i][2]

                placeImage = Image.new("RGBA", (workSize, workSize), color=(255, 255, 255, 0))
                placeImage.paste(work_image, point)
                fullImage = Image.alpha_composite(fullImage, placeImage)

        return fullImage

    def addImage(self, image):
        if self.__placed == self.__imagesPerPage:
            return False
        
        if self.__thumbnailSize == 0:
            self.__thumbnailSize = image.getThumbnailSize()

        self.__images.append(image)

        workSize = self.__thumbnailSize

        if self.__thumbnail is None:
            self.__thumbnail = Image.new("RGBA", (workSize, workSize), color=(0, 0, 0, 255))
            
            draw = ImageDraw.Draw(self.__thumbnail)
            draw.ellipse([0, 0, workSize, workSize], fill=(0, 0, 0, 0))
        
        # Első kép elhelyezése középre ha a kártyán lévő képek száma nagyobb mint 3
        if self.__imagesPerPage > 3 and self.__placed == 0:
            rotation = random.randrange(0, 360)
            self.__modTable.append([rotation])
            work_image = image.getCropImage().rotate(rotation, expand=True)

            sizeMod = random.uniform(1.3, 2.0)

            if work_image.width > work_image.height:
                scale = ((workSize / 5) / work_image.width) * sizeMod
            else:
                scale = ((workSize / 5) / work_image.height) * sizeMod

            self.__modTable[0].append(scale * (self.__fullImageSize / self.__thumbnailSize))

            size = (
                int(work_image.width * scale),
                int(work_image.height * scale)
            )

            work_image = work_image.resize(size)

            pointMod = (
                random.uniform(0.9, 1.1),
                random.uniform(0.9, 1.1)
            )

            point = (
                int(((workSize / 2) - (work_image.width / 2)) * pointMod[0]),
                int(((workSize / 2) - (work_image.height / 2)) * pointMod[1])
            )

            self.__modTable[0].append(
                (
                    int((self.__fullImageSize / 2) - (self.__thumbnailSize / 2 - point[0]) * (self.__fullImageSize / self.__thumbnailSize)),
                    int((self.__fullImageSize / 2) - (self.__thumbnailSize / 2 - point[1]) * (self.__fullImageSize / self.__thumbnailSize)),
                )
            )

            self.__thumbnail.paste(work_image, point)
        else:
            done = False
            pre_work_image = image.getCropImage()

            modTableId = len(self.__modTable)
            self.__modTable.append([0])

            trying = 0

            while done == False:
                rotation = random.randrange(0, 360)
                self.__modTable[modTableId][0] = rotation
                work_image = pre_work_image.rotate(rotation, expand=True)

                sizeMod = random.uniform(1.3, 2.0)

                if work_image.width > work_image.height:
                    scale = ((workSize / 5) / work_image.width) * sizeMod
                else:
                    scale = ((workSize / 5) / work_image.height) * sizeMod

                size = (
                    int(work_image.width * scale),
                    int(work_image.height * scale)
                )

                work_image = work_image.resize(size)

                pointMod = (
                    random.uniform(0.9, 1.1),
                    random.uniform(0.9, 1.1)
                )

                point = (
                    int((workSize / 5) * 4 * pointMod[0]),
                    int((workSize / 2) * pointMod[1])
                )

                rotation = 360 / (self.__imagesPerPage if self.__imagesPerPage == 3 else self.__imagesPerPage - 1)
                rotation = rotation * self.__placed

                point = self.__rotatePoint(workSize / 2, point, rotation)

                point = (
                    point[0] - int((work_image.width + 10) / 2),
                    point[1] - int((work_image.height + 10) / 2)
                )

                tmp_workImage = work_image.resize((work_image.width + 10, work_image.height + 10))

                if work_image.width + point[0] > workSize or work_image.height + point[1] > workSize:
                    trying += 1
                    continue

                placeImage = Image.new("RGBA", (workSize, workSize), color=(0, 0, 0, 0))
                placeImage.paste(tmp_workImage, point)
                if not self.__checkOverlap(placeImage):
                    point = (
                        point[0] + 5,
                        point[1] + 5
                    )

                    self.__modTable[modTableId].append(scale * (self.__fullImageSize / self.__thumbnailSize))
                    self.__modTable[modTableId].append(
                        (
                            int((self.__fullImageSize / 2) - (self.__thumbnailSize / 2 - point[0]) * (self.__fullImageSize / self.__thumbnailSize)),
                            int((self.__fullImageSize / 2) - (self.__thumbnailSize / 2 - point[1]) * (self.__fullImageSize / self.__thumbnailSize)),
                        )
                    )
                    placeImage = Image.new("RGBA", (workSize, workSize), color=(0, 0, 0, 0))
                    placeImage.paste(work_image, point)
                    self.__thumbnail = Image.alpha_composite(self.__thumbnail, placeImage)
                    done = True

                trying += 1

            if trying == 10:
                self.__images.pop(-1)
                return -1

        self.__placed += 1

    def __rotatePoint(self, origin, point, angle):
        angle = math.radians(angle)
        px, py = point

        sinA = math.sin(angle)
        cosA = math.cos(angle)

        qx = origin + (cosA * (px - origin)) + (sinA * (py - origin))
        qy = origin - (sinA * (px - origin)) + (cosA * (py - origin))
        return (int(qx), int(qy))

    def __checkOverlap(self, image):
        thumbnailNp = np.array(self.__thumbnail)
        imageNp = np.array(image)

        array = np.logical_and(thumbnailNp, imageNp)

        return np.any(array)