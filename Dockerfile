FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 git mercurial subversion && \
    apt-get clean

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    /opt/conda/bin/conda clean -afy

# Copy repo
RUN mkdir masktextspotter
#COPY api/ configs/ maskrcnn_benchmark/ outputs/ deploy.sh requirements-api.txt setup.py masktextspotter
COPY . masktextspotter/

# Install python dependencies
RUN conda install ipython pip
RUN pip install ninja yacs cython matplotlib tqdm opencv-python shapely scipy tensorboardX

# Install PyTorch
RUN conda install pytorch torchvision cudatoolkit=10.0 -c pytorch

# Install API dependencies
RUN pip install --no-cache-dir -r masktextspotter/requirements-api.txt

# build
WORKDIR masktextspotter
RUN python setup.py build develop

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 5000
CMD /masktextspotter/deploy.sh
