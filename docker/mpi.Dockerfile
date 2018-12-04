FROM nvidia/cuda:9.0-cudnn7-devel-ubuntu16.04
ARG PYTHON_VERSION=3.6

RUN apt-get update && apt-get install -y --no-install-recommends \
         build-essential \
         cmake \
         git \
         curl \
         vim \
         wget \
         ca-certificates \
         openssh-client \
         libjpeg-dev \
         libpng-dev &&\
     rm -rf /var/lib/apt/lists/*

# Install open-mpi
RUN wget https://www.open-mpi.org/software/ompi/v3.0/downloads/openmpi-3.0.0.tar.gz && \
    gunzip -c openmpi-3.0.0.tar.gz | tar xf - && \
    cd openmpi-3.0.0 && \
    ./configure --prefix=/home/.openmpi --with-cuda && \
    make all install

ENV PATH="$PATH:/home/.openmpi/bin"
ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/home/.openmpi/lib/"

RUN ompi_info --parsable --all | grep mpi_built_with_cuda_support:value

# install miniconda
RUN curl -o ~/miniconda.sh -O  https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh  && \
     chmod +x ~/miniconda.sh && \
     ~/miniconda.sh -b -p /opt/conda && \
     rm ~/miniconda.sh && \
     /opt/conda/bin/conda update conda && \
     /opt/conda/bin/conda install -y python=$PYTHON_VERSION pandas scikit-learn scikit-image pyyaml ipython cython tqdm && \
     /opt/conda/bin/conda clean -ya
ENV PATH /opt/conda/bin:$PATH
# This must be done before pip so that requirements.txt is available
WORKDIR /opt/pytorch

RUN git clone --recursive https://github.com/pytorch/pytorch

RUN TORCH_CUDA_ARCH_LIST="3.5 5.2 6.0 6.1 7.0+PTX" TORCH_NVCC_FLAGS="-Xfatbin -compress-all" \
    CMAKE_PREFIX_PATH="$(dirname $(which conda))/../" \
    cd pytorch/ && \
    pip install -v .

RUN /opt/conda/bin/conda config --set ssl_verify False
RUN pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org torchvision
RUN pip install setproctitle

RUN mkdir /mnt/hpa-data
WORKDIR /home/hpa
ADD train.py ./train.py
ADD src/ ./src
ADD service-account.json /var/service-account.json

# ENTRYPOINT ["mpirun", "-n", "4", "--allow-run-as-root", "python", "-u", "train.py"]
