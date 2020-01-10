import xml.etree.ElementTree as ET
import os
import argparse
from sklearn.model_selection import train_test_split

# get className_list
def get_classNameList(txtFilePath):
    with open(txtFilePath, 'r', encoding='utf8') as file:
        fileContent = file.read()
        line_list = [k.strip() for k in fileContent.split('\n') if k.strip()!='']
        className_list= sorted(line_list, reverse=False)
    return className_list  
    
# get the file path
import os
def get_filePathList(dirPath, partOfFileName=''):
    allFileName_list = list(os.walk(dirPath))[0][2]
    fileName_list = [k for k in allFileName_list if partOfFileName in k]
    filePath_list = [os.path.join(dirPath, k) for k in fileName_list]
    return filePath_list
    
# command line arguments
import argparse
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dirPath', type=str, help='文件夹路径', default='../resources/images_416x416')    
    parser.add_argument('-s', '--suffix', type=str, default='.jpg')
    parser.add_argument('-c', '--class_txtFilePath', type=str, default='../resources/category_list.txt')
    argument_namespace = parser.parse_args()
    return argument_namespace  
    

if __name__ == '__main__':
    argument_namespace = parse_args()
    dataset_dirPath = argument_namespace.dirPath
    assert os.path.exists(dataset_dirPath), 'not exists this path: %s' %dataset_dirPath
    suffix = argument_namespace.suffix
    class_txtFilePath = argument_namespace.class_txtFilePath
    xmlFilePath_list = get_filePathList(dataset_dirPath, '.xml')
    className_list = get_classNameList(class_txtFilePath)
    train_xmlFilePath_list, test_xmlFilePath_list = train_test_split(xmlFilePath_list, test_size=0.1)
    dataset_list = [('dataset_train', train_xmlFilePath_list), ('dataset_test', test_xmlFilePath_list)]
    for dataset in dataset_list:
        txtFile_path = '%s.txt' %dataset[0]
        txtFile = open(txtFile_path, 'w')
        for xmlFilePath in dataset[1]:
            jpgFilePath = xmlFilePath.replace('.xml', '.jpg')
            txtFile.write(jpgFilePath)
            with open(xmlFilePath) as xmlFile:
                xmlFileContent = xmlFile.read()
            root = ET.XML(xmlFileContent)
            for obj in root.iter('object'):
                className = obj.find('name').text
                if className not in className_list:
                    print('error!! className not in className_list')
                    continue
                classId = className_list.index(className)
                bndbox = obj.find('bndbox')
                bound = [int(bndbox.find('xmin').text), int(bndbox.find('ymin').text),
                        int(bndbox.find('xmax').text), int(bndbox.find('ymax').text)]
                txtFile.write(" " + ",".join([str(k) for k in bound]) + ',' + str(classId))
            txtFile.write('\n')
        txtFile.close()

