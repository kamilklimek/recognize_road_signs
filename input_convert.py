from scipy.misc import imread
from scipy.misc import imshow
import PIL as pillow
import numpy as np
try:
    import Image
except ImportError:
    from PIL import Image

class_directories_name = ["%05d" % i for i in range(11)]

class Detail:
    def __init__(self, file_name, width, height, x_start, y_start, x_end, y_end):
        self.width = int(width)
        self.file_name = file_name
        self.height = int(height)
        self.x_start = int(x_start)
        self.y_start = int(y_start)
        self.x_end = int(x_end)
        self.y_end = int(y_end)
    
    def get_file_name(self):
        return self.file_name

    def get_size(self):
        return (self.width, self.height)

    def get_start_position(self):
        return (self.x_start, self.y_start)

    def get_end_position(self):
        return (self.x_end, self.y_end)

    def __str__(self):
        return "Filename: " + str(self.get_file_name()) + str(self.get_start_position()) + str(self.get_end_position())

    @staticmethod
    def str_to_detail(line: str):
        values = line.split(";")
        return Detail(values[0], values[1], values[2], values[3], values[4], values[5], values[6])


class Img:
    def __init__(self, image: list, width: int, height: int):
        self.image = image
        self.width = width
        self.height = height

    def get_size(self):
        return self.width, self.height

    def get_image(self):
        return self.image

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def __str__(self):
        return "Width: " + str(self.width) + ", height: " + str(self.height) + ", image: " + str(self.image)


def read_class(directory_name: str):
    csv_name = "train_sign/" + directory_name + "/GT-" + directory_name + ".csv"      
    csv_file = open(csv_name, "r")
    class_details = []
    [class_details.append(Detail.str_to_detail(line)) for line in csv_file.readlines()[1:]]
    return class_details


def read_image(class_directory_name: str, detail: Detail):
    image_path = "train_sign/" + class_directory_name +  "/" + detail.get_file_name()
    image_handler = open(image_path, "rb")

    start_position = detail.get_start_position
    end_position = detail.get_end_position
    image = imread(image_path)
    return image

def read_sign(class_directory_name: str, detail: Detail):
    image = read_image(class_directory_name, detail)
    start_position = detail.get_start_position()
    size = detail.get_size()

    x = start_position[0]
    y = start_position[1]

    width = size[0]
    height = size[1]

    image = image[x-width:x+width][y-height:y+height]

    return Img(image, width, height)

def resize_sign(image: Img, destination_size: tuple):
    img = Image.fromarray(image)
    resize_img = img.resize(destination_size)
    image.image = resize_img
    return image

class_details = []
[class_details.append(read_class(file_name)) for file_name in class_directories_name]

sign = read_sign(class_directories_name[10], class_details[10][44])
imshow(resize_sign(sign, (25, 25)))