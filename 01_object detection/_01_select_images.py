import os
import random
from PIL import image

import cv2
import argparse

# get the file path
def get_filePathList(dirPath, partOfFileName=''):
    # cd = os.getcwd()
    # find all the file in the directory
    allFileName_list = os.listdir(dirPath)
    fileName_list = [k for k in allFileName_list if partOfFileName in k]
    filePath_list = [os.path.join(dirPath, k) for k in fileName_list]
    return filePath_list

# select the images from the documents
def select_qualifiedImages(in_dirPath, out_dirPath, in_suffix, out_suffix, sample_number, required_width, required_height):
    imageFilePath_list = get_filePathList(in_direPath, in_suffix)
    random.shuffle(imageFilePath_list)
    if not os.path.isdir(out_dirPath):
        os.makedirs(out_dirPath)
    count = 0

    for i, imageFilePath in enumerate(imageFilePath_list):
        image = Image.open(imageFilePath)
        image_width, image_height = image.size
        if image_width >= required_width and image_height >= required_height:
            count += 1
            # output file direction
            out_imageFilePath = os.path.join(out_dirPath, '%03d%s' % (count, out_suffix))
            image_ndarray = cv2.imread(imageFilePath)
            cv2.imwrite(out_imageFilePath, image_ndarray)
        
        if count == sample_number:
            break

# change the command line argument
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--in_dir', type=str, default='../resources/n01440764', help='input')
    parser.add_argument('-o', '--out_dir', type=str, default='../resources/selected_images', help='output')
    parser.add_argument('--in_suffix', type=str, default='.JPEG')
    parser.add_argument('--out_suffix', type=str, default='.jpg')
    parser.add_argument('-n', '--number', type=int, default=200)
    parser.add_argument('-w', '--width', type=int, default=416)
    parser.add_argument('-he', '--height', type=int, default=416)
    argument_namespace = parser.parse_args()
    return argument_namespace


# get 200 qualified sample and put in the selected_images file

if __name__ == "__main__":
    argument_namespace = parse_args()
    in_dirPath = argument_namespace.in_dir.strip()
    assert os.path.exists(in_dirPath), 'not exists this path: %s' %in_dirPath
    out_dirPath = argument_namespace.out_dir.strip()
    sample_number = argument_namespace.number
    in_suffix = argument_namespace.in_suffix.strip()
    in_suffix = '.' + in_suffix.lstrip('.')
    out_suffix = argument_namespace.out_suffix.strip()
    out_suffix = '.' + out_suffix.lstrip('.')
    select_qualifiedImages(in_dirPath, out_dirPath, in_suffix, out_suffix, sample_number, required_width, required_height)
    out_dirPath = os.path.abspath(out_dirPath)
    print('the qualified picture and put in the file: %s' %out_dirPath)
    imageFilePath_list = get_filePathList(out_dirPath, out_suffix)
    selectedImages_number = len(imageFilePath_list)
    print('the number of qualified picture: %d' %selectedImages_number)
    if selectedImages_number < sample_number:
        print('the selected number of qualified picture is not enough < %d, need decrease width and height' %sample_number)



