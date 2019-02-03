# Use https://docs.nvidia.com/deeplearning/dgx/pytorch-release-notes/running.html#running
FROM nvcr.io/nvidia/pytorch:18.08-py3

RUN pip install gsutil
RUN pip install setproctitle
RUN conda install -y pandas
RUN conda install -c conda-forge scikit-image

# reinstall torchvision so that it pulls in the latest version of torch
RUN conda install -y -f torchvision

RUN mkdir /workspace/
COPY . /workspace/

ENTRYPOINT ["/workspace/train.sh"]
