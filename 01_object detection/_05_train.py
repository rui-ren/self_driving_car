# import library

import os 
import numpy as np 
import keras.backend as k
from keras.layers import Input, Lambda 
from keras.model import model
# import yolo3 mode.py, utils.py

from yolo3.model import preprocess_true_boxes, yolo_body, yolo_loss
from yolo3.utils import get_random_data

# get the category_list
def get_categoryList(txtFilePath):
    with open(txtFilePath, 'r', encoding='utf8') as file:
        fileContent = file.read()
    line_list = [k.strip() for k in fileContent.split('\n') if k.strip() != '']
    category_list = sorted(line_list, reverse=False)
    return category_list

# anchor file get anchor_ndarray
def get_anchorNdarray(anchor_txtFilePath):
    with open(anchor_txtFilePath) as file:
        anchor_ndarray = [float(k) for k in file.read().split(',')]
    return np.array(anchor_ndarray).reshape(-1,2)


# Yolov2 model, yolo_body inference, cnn

def create_model(input_shape,
                anchor_ndarray,
                num_classes,
                load_pretrained=True,
                freeze_body=False,
                weights_h5FilePath='../resources/saved_models/trained_weights.h5'):
    k.clear_session()
    image_input = input_shape
    num_anchors = len(anchor_ndarray)
    y_true = [Input(shape=(height //k,
                            width //k,
                            num_anchors //3,
                            num_classes + 5)) for k in [32, 16, 8]]
    model_body = yolo_body(image_input, num_anchors//3, num_classes)
    print('Create YOLOv3 model with {} anchors and {} classes.'.format(num_anchors, num_classes))

    if load_pretrained and os.path.exists(weights_h5FilePath):
        model_body.load_weights(weights_h5FilePath, by_name=True, skip_mismatch=True)
        print('Load weightf from this path: {}.'.format(weights_h5FilePath))
        if freeze_body:
            num = len(model_model.layers) - 7
            for i in range(num):
                model_body.layers[i].trainable = False
            print('Free the first {} layers of total {} layers.'.format(num, len(model_body.layers)))

    model_loss = Lambda(yolo_loss, 
                        output_shape=(1, ),
                        name='yolo_loss',
                        arguments={
                            'anchors': anchor_ndarray,
                            'num_classes': num_classes,
                            'ignore_thresh': 0.5
                        })(
                            [*model_body.output, *y_true]
                        )
    model = Model([model_body.input, *y_true], model_loss)
    return model


def train(
        model,
        annotationFilePath,
        input_shape,
        anchor_ndarray,
        num_classes,
        logDirPath='../resources/saved_models/'
        ):
    
    model.compile(optimizer='adam',
                loss={'yolo_loss': lambda y_true, y_pred: y_pred})

    # train and dev
    batch_size = 2 * num_classes
    val_split = 0.05
    with open(annotationFilePath) as file:
        lines = file.readlines()
    np.random.shuffle(lines)
    num_val = int(len(lines)*val_split)
    num_train = len(lines) - num_val
    print('Train on {} samples, val on {} samples, with batch size {}'.format(num_train, num_val, batch_size))

    # model generator
    model.fit_generator(
        data_generator(lines[:num_train], batch_size, input_shape, anchor_ndarray, num_classes)
        steps_per_epoch=max(1, num_train//batch_size),
        validation_data=data_generator(lines[num_train:], batch_size, input_shape, anchor_ndarray, num_classes)
        validation_steps=max(1, num_val//batch_size),
        epochs=200,
        initial_epoch=0
    )

    # save model
    if not os.path.isdir(logDirPath):
        os.makedirs(logDirPath)
    model.savedPath = os.path.join(logDirPath, 'trained_weights.h5')
    model.save_weights(model_savedPath)


# generator model generator image

def data_generator(annotationFilePath, batch_size, input_shape, anchors, num_classes):
    n = len(annotation_lines)
    np.random.shuffle(annotation_lines)
    i = 0
    whiel True:
        image_data = []
        box_data = []
        for b in range(batch_size):
            i %= n
            image, box = get_random_data(annotation_lines[i], input_shape, random=True)
            image_data.append(image)
            box_data.append(box)
            i += 1
        image_data = np.array(image_data)
        box_data = np.array(box_data)
        y_true = preprocess_true_boxes(box_data, input_shape, anchors, num_classes)
        yield [image_data, *y_true], np.zeros(batch_size)


import argparse
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--width', type=int, default=416)
    parser.add_argument('-he', '--height', type=int, default=416)
    parser.add_argument('-c', '--class_txtFilePath', type=str, default='../resorces/category_list.txt')
    parser.add_argument('-a', '--anchor_txtFilePath', type=str, default='./model_data/yolo_anchors.txt') 
    argument_namespace = parser.parser_args()
    return argument_namespace

if __name__ == "__main__":
    argument_namespace = parse_args()
    class_txtFilePath = argument_namespace.class_txtFilePath
    anchor_txtFilePath = argument_namespace.anchor_txtFilePath
    category_list = get_categoryList(class_txtFilePath)
    anchor_ndarray = get_anchorNdarray(anchor_txtFilePath)
    width = argument_namespace.width
    height = argument_namespace.height
    input_shape = (width, height)  # 
    model = create_model(input_shape, anchor_ndarray, len(category_list))
    annotationFilePath = 'dataset_train.txt'
    train(model, annotationFilePath, input_shape, anchor_ndarray, len(category_list))

    

