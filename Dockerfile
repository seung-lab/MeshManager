FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN apt-get update && apt-get install --yes build-essential libgl1-mesa-dev mesa-utils libgl1-mesa-glx
RUN apt-get -y install cmake libboost-all-dev libblas-dev liblapack-dev

RUN mkdir -p /home/nginx/.cloudvolume/secrets && chown -R nginx /home/nginx && usermod -d /home/nginx -s /bin/bash nginx
COPY requirements.txt /app/.
RUN  pip install -r requirements.txt
#RUN pip install git+https://github.com/seung-lab/cloud-volume.git@graphene#egg=cloud-volume

RUN pip show cloud-volume
COPY . /app

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

# MeshParty
WORKDIR /usr/local/ 
RUN git clone https://github.com/sdorkenw/MeshParty.git
WORKDIR /usr/local/MeshParty
RUN pip install -r requirements.txt
RUN pip install . 


WORKDIR /app

ENTRYPOINT [ "python" ]
CMD ["run.py"]
