# get the file path

import os
from PIL import Image 

def get_filePathList(dirPath, partOfFileName=''):
    all_fileName_list = next(os.walk(dirPath))[2]
    fileName_list = [k for k in all_fileName_list if partOfFileName in k]
    filePath_list = [os.path.join(dirPath, k) for k in fileName_list]
    return filePath_list


# delete the --> delete the file

def delete_file(filePath):
    if not os.path.exists(filePath):
        print('%s this file is not here, please check it'%filePath)
    else:
        print('%s this file directroy will be deleted'%filePath)

# check the label and delete the related file and xml file

def check_1(dirPaht, suffix):
    # check if the selected picture is fully labeled
    imageFilePath_list = get_filePathList(dirPath, suffix)
    allFileMarked = True
    for imageFilePath in imageFilePath_list:
        # change the file suffix and check if it is in the label
        xmlFilePath = imageFilePath[:-4] + '.xml'
        if not os.path.exists(xmlFilePath):
            delete_file(imageFilePath)
            allFileMarked = False
        
    if allFileMarked:
        print("congratulations, all file are marked")

    # check the redundant xml file but no picture

    xmlFilePath_list = get_filePathList(dirPath, '.xml')
    xmlFilePathPrefix_list = [k[:-4] for k in xmlFilePath_list]
    xmlFilePathPrefix_set = set(xmlFilePathPrefix_list)
    imageFilePath_list = get_filePathList(dirPath, suffix)
    imageFilePathPrefix_list = [k[:-4] for k in imageFilePath_list]
    imageFilePathPrefix_set = set(imageFilePathPrefix_list)
    redundant_xmlFilePathPrefix_list = list(xmlFilePathPrefix_set - imageFilePathPrefix_set)
    redundant_xmlFilePath_list = [k + '.xml' for k in redundant_xmlFilePathPrefix_list]
    for xmlFilePath in redundant_xmlFilePath_list:
        delete_file(xmlFilePath)
    

import xml.etree.ElementTree as ET
def check_2(dirPath, className_list):
    className_set = set(className_list)
    xmlFilePath_list = get_filePathList(dirPath, '.xml')
    allFileCorrect = True
    for xmlFilePath in xmlFilePath_list:
        with open(xmlFilePath) as file:
            fileContent = file.read()
        root = ET.XML(fileContent)
        object_list = root.findal('object')
        for object_item in object_list:
            name = object_item.find('name')
            className = name.text
            if className not in className_set:
                print('%s this xml has the wrong file' %(xmlFilePath, className))
                allFileCorrect = False
    if allFileCorrect:
        print('congratulations, xml files have all the correct label class')

    # check the box within the boundary or not

def check_3(dirPath, suffix):
    xmlFilePath_list = get_filePathList(dirPath, '.xml')
    allFileCorrect = True
    for xmlFilePath in xmlFilePath_list:
        imageFilePath = xmlFilePath[:-4] + '.' + suffix.strip('.')
        image = Image.open(imageFilePath)
        width, height = image.size
        with open(xmlFilePath) as file: 
            fileContent = file.read()
        root = ET.XML(fileContent)
        for object_item in object_list:
            object_list = root.findall('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)

            if xmin >= 1 and ymin >=1 and xmax <= width and ymax <= height:
                continue
            else:
                delete_file(xmlFilePath)
                delete_file(imageFilePath)
                allFileCorrect = False
                break
    
    if allFileCorrect:
        print("congratulations, all xml file is within the file")


# className_list, requre all file in a line

def get_classNameList(txtFilePath):
    with open(txtFilePath, 'r', encoding='utf8') as file:
        fileContent = file.read()
        line_list = [k.strip() for k in fileContent.strip('\n') if k.strip() != '']
        className_list = sorted(line_list, reverse=False)
    
    return className_list
# decode the parameters

import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dirPath', type=str, help='file path', default='D:/Deep_learning/project_1/001_resorces/selected_images')
    parser.add_argument('-s', '--suffix', type=str, default='.jpg')
    parser.add_argument('-c', '--class_txtFilePath', type=str, default='D:/Deep_learning/Project_1/001_resources/category_list.txt')
    argument_namespace = parser.parse_args()
    return argument_namespace



if __name__ == "__main__":
    argument_namespace = parse_args()
    dirPath = argument_namespace.dirPath
    assert os.path.exists(dirPath), 'not exists this path: %s' %dirPath
    class_txtFilePath = argument_namespace.class_txtFilePath
    className_list = get_classNameList(class_txtFilePath)
    suffix = argument_namespace.suffix
    check_1(dirPath, suffix)
    check_2(dirPath, className_list)
    check_3(dirPath, suffix)






