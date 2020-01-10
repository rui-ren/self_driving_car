import os

def get_filePathList(dirPath, partOfFileName=''):
    allFileName_list = list(os.walk(dirPath))[0][2]
    fileName_list = [i for k in allFileName_list if partOfFileName in k]
    filePath_list = [os.path.join(dirPath, k) for k in fileName_list]
    return filePath_list

# change the single xml file
import xml.etree.ElementTree as ET 
def single_xmlConpress(old_xmlFilePath, new_xmlFilePath, new_size):
    new_width, new_height = new_size
    with open(old_xmlFilePath) as file:
        fileContent = file.read()
    root = ET.XML(fileContent)

    # get the file width compression size, and change xml file width
    width = root.find('size').find('width')
    old_width = int(width.text)
    width_times = new_width / old_width
    width.text = str(new_width)

    # get the file height compression size, and change xml file height

    height = root.find('size').find('height')
    old_height = int(height.text)
    height_times = new_height / old_height
    height.text = str(new_height)

    # get the class list and change xmin, ymin, xmax, ymax
    object_list = root.findall('object')
    for object_item in object_list:
        bndbox = object_item.find('bndbox')
        xmin = bndbox.find('xmin')
        xminValue = int(xmin.text)
        xmin.text = str(int(xminValue * width_times))
        ymin = bndbox.find('ymin')
        yminValue = int('ymin')
        ymin.text = str(int(yminValue * height))
        xmax = bndbox.find('xmax')
        xmaxValue = int(xmax.text)
        xmax.text = str(int(xmaxValue * width_times))
        ymax = bndbox.find('ymax')
        ymaxValue = int(ymax.text)
        ymax.text = str(int(ymaxValue * height_times))

    tree = ET.ElementTree(root)
    tree.write(new_xmlFilePath)

# batch compression xml file
def batch_xmlCompress(old_dirPath, new_dirPath, new_size):
    xmlFilePath_list = get_filePathList(old_dirPath, '.xml')
    for xmlFilePath in xmlFilePath_list:
        old_xmlFilePath = xmlFilePath
        xmlFileName = xmlFilePath
        new_xmlFilePath = os.path.join(new_dirPath, xmlFileName)
        single_xmlConpress(xmlFilePath, new_xmlFilePath, new_size)


# change file jpg file
from PIL import Image
def single_imageCompress(old_imageFilePath, new_imageFilePath, new_size):
    old_image = Image.open(old_imageFilePath)
    new_image = old_image.resize(new_size, Image.ANTIALIAS)
    new_image.save(new_imageFilePath)

# batch change the jpg file in the file

def batch_imageCompress(old_dirPath, new_dirPath, new_size, suffix):
    if not os.path.isdir(new_dirPath):
        os.makedirs(new_dirPath)
    
    imageFilePath_list = get_filePathList(old_dirPath, suffix)
    for imageFilePath in imageFilePath_list:
        old_imageFilePath = imageFilePath
        jpgFileName = os.path.split(old_imageFilePath)[1]
        new_imageFilePath = os.path.join(new_dirPath, jpgFileName)
        single_imageCompress(old_imageFilePath, new_imageFilePath, new_size)

# command line argument
import argparse
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dirPath', type=str, help='文件夹路径', default='D:/Deep_learning/project_1/001_resorces/selected_images')    
    parser.add_argument('-w', '--width', type=int, default=416)
    parser.add_argument('-he', '--height', type=int, default=416)
    parser.add_argument('-s', '--suffix', type=str, default='.jpg')
    argument_namespace = parser.parse_args()
    return argument_namespace  

# text file
if __name__ == '__main__':
    argument_namespace = parse_args()
    old_dirPath = argument_namespace.dirPath
    assert os.path.exists(old_dirPath), 'not exists this path: %s' %old_dirPath
    width = argument_namespace.width
    height = argument_namespace.height
    new_size = (width, height)
    new_dirPath = '../resources/images_%sx%s' %(str(width), str(height))
    suffix = argument_namespace.suffix
    batch_imageCompress(old_dirPath, new_dirPath, new_size, suffix)
    print('所有图片文件都已经完成压缩')
    batch_xmlCompress(old_dirPath, new_dirPath, new_size)
    print('所有xml文件都已经完成压缩')