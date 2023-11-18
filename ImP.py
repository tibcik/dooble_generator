#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw
from PIL import ImageTk

class ImP():
    def __init__(self, imagePath, image = None):
        self.__imagePath = imagePath
        self.__thumbnailSize = 600
        self.__thumbnailImage = None

        if image is None:
            self.__createThumbnail()
        else:
            self.__thumbnailImage = image

    def __createThumbnail(self):
        self.__thumbnailImage = Image.new("RGBA", (self.__thumbnailSize, self.__thumbnailSize), color=(0, 0, 0, 0))

        image = Image.open(self.__imagePath)

        if image.width > image.height:
            scale = self.__thumbnailSize / image.width
        else:
            scale = self.__thumbnailSize / image.height
        size = (int(image.width * scale), int(image.height * scale))

        image = image.resize(size)

        point = (
            int((self.__thumbnailSize - image.width) / 2),
            int((self.__thumbnailSize - image.height) / 2)
        )

        self.__thumbnailImage.paste(image, point)

    def getThumbnailSize(self):
        return self.__thumbnailSize

    def getImagePath(self):
        return self.__imagePath

    def getImageTk(self, size=None):
        if size is None:
            return ImageTk.PhotoImage(self.__thumbnailImage)
        
        return ImageTk.PhotoImage(self.__thumbnailImage.resize(size))

    def getImage(self, thumbnail=True):
        if thumbnail:
            return self.__thumbnailImage
        
        return Image.open(self.__imagePath)

    def getBackImage(self):
        fullImage = Image.new("RGBA", (self.__thumbnailSize, self.__thumbnailSize), color=(255, 255, 255, 0))
            
        draw = ImageDraw.Draw(fullImage)
        draw.ellipse([0, 0, self.__thumbnailSize, self.__thumbnailSize], width=1, outline=(0, 0, 0, 255))

        placeImage = Image.new("RGBA", (self.__thumbnailSize, self.__thumbnailSize), color=(255, 255, 255, 0))
        placeImage.paste(self.__thumbnailImage, (0, 0))

        return Image.alpha_composite(fullImage, placeImage)

    def getCropImage(self, thumbnail=True):
        if thumbnail:
            cropBox = self.__crop(self.__thumbnailImage)

            return self.__thumbnailImage.crop(cropBox)
        
        image = Image.open(self.__imagePath, mode="RGBA")
        cropBox = self.__crop(image)

        return image.crop(cropBox)

    def __crop(self, image):
        return (
            self.__cropLeft(image),
            self.__cropUp(image),
            self.__cropRight(image),
            self.__cropDown(image)
        )

    def __cropLeft(self, image):
        for x in range(image.width):
            for y in range(image.height):
                if image.getpixel((x, y))[3] != 0:
                    return x

    def __cropRight(self, image):
        for x in range((image.width - 1), -1, -1):
            for y in range(image.height):
                if image.getpixel((x, y))[3] != 0:
                    return x

    def __cropUp(self, image):
        for y in range(image.height):
            for x in range(image.width):
                if image.getpixel((x, y))[3] != 0:
                    return y
                
    def __cropDown(self, image):
        for y in range((image.height - 1), -1, -1):
            for x in range(image.width):
                if image.getpixel((x, y))[3] != 0:
                    return y