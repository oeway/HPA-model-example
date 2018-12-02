import csv
import numpy as np

from torchvision import transforms
from torch.utils.data import DataLoader
from tqdm import tqdm

from .rather_small_net import RatherSmallNet
from .resnet_152 import Resnet152
from .loss_functions import f1_loss, binary_cross_entropy_with_logits
from .transforms import *
from .datasets import TrainImageDataset, TestImageDataset

def get_transform():
    return transforms.Compose(
                    [CombineColors(),
                     ToTensor()])

def get_pretrained_pytorch_model_transform(): 
    return transforms.Compose(
                [CombineColors(),
                 ToTensor(),
                 Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
                ])

def get_dataset(image_dir, label_file, train=True, idxs=None, pretrained=False):
    if pretrained:
        transform = get_pretrained_pytorch_model_transform()
    else:
        transform = get_transform()
    if train:
        dataset = TrainImageDataset(
                         image_dir=image_dir,
                         label_file=label_file,
                         transform=transform,
                         idxs=idxs)
    else:
        dataset = TestImageDataset(
                         image_dir=image_dir,
                         transform=transform,
                         idxs=idxs)
    return dataset

def get_prediction_dataloader(image_dir, **kwargs):
    return DataLoader(dataset = get_prediction_dataset(image_dir),
        shuffle=False,
        **kwargs
    )

def get_prediction_dataset(image_dir):
    return TestImageDataset(
        image_dir=image_dir,
        transform=get_transform())

def get_train_test_split(train_image_dir,
                         train_image_csv,
                         val_split,
                         n_subsample,
                         pretrained,
                         **kwargs
                         ):
    with open(train_image_csv, 'r') as f:
        n_images = sum(1 for row in f.readlines()) - 1 # -1 for header row
    if n_subsample != 0:
        arr = np.random.choice(n_images, n_subsample, replace=False)
        train_idxs = arr[:int(n_subsample * (1 - val_split))]
        dev_idxs = arr[int(n_subsample * (1 - val_split)):]
    else:
        arr = np.random.choice(n_images, n_images, replace=False)
        train_idxs = arr[:int(n_images * (1 - val_split))]
        dev_idxs = arr[int(n_images * (1 - val_split)):]

    trainset = get_dataset(train_image_dir, train_image_csv, idxs=train_idxs, pretrained=pretrained)
    devset = get_dataset(train_image_dir, train_image_csv, idxs=dev_idxs, pretrained=pretrained)

    # trainset = []
    # testset = []
    # print('getting training set...')
    # for i in tqdm(train_idxs):
    #     sample = dataset[i]
    #     trainset.append(sample)
    # print('getting testing set...')
    # for i in tqdm(test_idxs):
    #     sample = dataset[i]
    #     testset.append(sample)
    trainloader = DataLoader(trainset, shuffle=True, **kwargs)
    devloader = DataLoader(devset, shuffle=False, **kwargs)
    return trainloader, devloader

def get_network(network_name="rather_small_net", pretrained=False):
    if network_name == "rather_small_net":
        return RatherSmallNet()
    elif network_name == "resnet_152":
        return Resnet152()

def get_loss_function(lf='bce'):
    if lf == 'bce':
        return binary_cross_entropy_with_logits
    elif lf == 'f1':
        return f1_loss
    else:
        raise ModuleNotFoundError('loss function not found')

def positive_predictions(predictions):
    positives = []
    for prediction in predictions:
        output = []
        i = 0
        for label in prediction:
            if(label == 1):
                output.append(str(i))
            i += 1
        positives.append(' '.join(output))

    return positives
