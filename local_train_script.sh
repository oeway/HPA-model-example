#!/bin/bash

python -u train.py -n "basicnet01" -d "hpa" --cuda True --train-images-path="./data/train_images" --test-images-path="./data/test_images" --nEpochs=1 --batchSz=32

echo "*** training complete. pod will stop in 10 minutes ***"

