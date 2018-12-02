#!/bin/bash

git checkout resnet152

python -u train.py -n "resnet_152" -d "hpa" --train-images-path="/hpakf-image-data/data/train_images" --test-images-path="/hpakf-image-data/data/test_images" --nEpochs=1 --batchSz=256  --use-cuda=yes

echo "*** training complete. pod will stop in 10 minutes ***"

sleep 600
