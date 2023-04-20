from PIL import Image
from PIL import ImageFilter

class ImageEditor:
    def __init__(self, filename):
        self.filename = filename
        self.original = None
        self.changed = list()

    def open(self):
        try:
            self.original = Image.open(self.filename)
        except:
            print('Файл не знайдено!')
        self.original.show()

    def do_left(self):
        rotated = self.original.transpose(Image.FLIP_LEFT_RIGHT)
        self.changed.append(rotated)

        temp_filename = self.filename.split('.')
        new_filename = temp_filename[0] + str(len(self.changed)) + "."+temp_filename[1]

        rotated.save(new_filename)


    def doBlack(self):
        blackImage = self.original.convert("L")
        self.changed.append(blackImage)

        temp_filename = self.filename.split('.')
        new_filename = temp_filename[0] + str(len(self.changed)) + "." + temp_filename[1]

        blackImage.save(new_filename)

image = ImageEditor("img.png")
image.open()

image.do_left()
image.doBlack()

for i in image.changed:
    i.show()