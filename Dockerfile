FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN apt-get update && apt-get install --yes build-essential libgl1-mesa-dev mesa-utils libgl1-mesa-glx
RUN apt-get -y install cmake libboost-all-dev libblas-dev liblapack-dev alien

RUN apt update && apt install --yes python3-pip


# download conda
#RUN curl -o ~/miniconda.sh -O  https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh  && \
#    chmod +x ~/miniconda.sh && \
#    ~/miniconda.sh -b -p /opt/conda && \
#    rm ~/miniconda.sh && \
#    /opt/conda/bin/conda update conda && \
#    /opt/conda/bin/conda install conda-build 
#ENV PATH /opt/conda/bin:$PATH


RUN pip install --upgrade pip
#RUN pip install werkzeug
RUN mkdir -p /home/nginx/.cloudvolume/secrets && chown -R nginx /home/nginx && usermod -d /home/nginx -s /bin/bash nginx
#COPY requirements.txt /app/.
COPY . /app
RUN  pip3 install -r requirements.txt
RUN pip install git+https://github.com/seung-lab/cloud-volume.git@fix_https_replace#egg=cloud-volume
RUN pip3 install .

#ASSIMP
WORKDIR /usr/local/assimp
RUN apt-get update -y
RUN apt-get update
RUN apt-get -y install cmake
RUN git clone https://github.com/assimp/assimp.git
WORKDIR /usr/local/assimp/assimp
RUN cmake CMakeLists.txt
RUN make -j16
RUN cp /usr/local/assimp/assimp/lib/libassimp.so /usr/local/lib

# Install some base packages
#RUN pip3 install numpy cython h5py scipy>=1.3.0 sklearn plyfile networkx multiwrapper trimesh && \
#    pip3 install pykdtree vtk pcst_fast shapely imageio pymeshfix>=0.12.3 annotationframeworkclient>=0.2.0

# Install embree
WORKDIR /usr/local/embree
ARG EMBREE_VERSION=2.17.5
ARG EMBREE_FILE=embree-${EMBREE_VERSION}.x86_64.rpm.tar.gz
ARG EMBREE_LIB=embree-lib-${EMBREE_VERSION}.x86_64.rpm
ARG EMBREE_DEVEL=embree-devel-${EMBREE_VERSION}.x86_64.rpm
ARG EMBREE_EX=embree-examples-${EMBREE_VERSION}.x86_64.rpm
RUN curl -L -O https://github.com/embree/embree/releases/download/v${EMBREE_VERSION}/${EMBREE_FILE} && \
    tar xzf ${EMBREE_FILE} && \
    rm ${EMBREE_FILE}
RUN alien *.rpm && dpkg -i *.deb && rm *.rpm
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:/usr/lib64
RUN apt-get -y install libtbb-dev

# Install pyembree from source
WORKDIR /usr/local
RUN git clone https://github.com/scopatz/pyembree.git
WORKDIR /usr/local/pyembree
RUN pip3 install .

RUN pip install git+https://github.com/seung-lab/cloud-volume.git@fix_https_replace#egg=cloud-volume

# MeshParty
#WORKDIR /usr/local/ 
#RUN git clone https://github.com/sdorkenw/MeshParty.git
#WORKDIR /usr/local/MeshParty
#RUN cat requirements.txt | sed -e '/^\s*pyembree.*$/d' -e '/^\s*$/d' > requirements.txt
#RUN pip3 install -r requirements.txt
#RUN pip3 install cloud-volume==0.53.6
#RUN conda install -c conda-forge pyembree
#RUN conda install -c anaconda flask flask-cors
#RUN pip3 install . 

RUN pip install jupyter jupyterlab
COPY jupyter_notebook_config.py /root/.jupyter/
EXPOSE 9999

WORKDIR /app

ENTRYPOINT [ "python" ]
CMD ["run.py"]
