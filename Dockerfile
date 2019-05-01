FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN apt-get update && apt-get install --yes build-essential libgl1-mesa-dev mesa-utils libgl1-mesa-glx
RUN apt-get -y install cmake libboost-all-dev libblas-dev liblapack-dev

RUN mkdir -p /home/nginx/.cloudvolume/secrets && chown -R nginx /home/nginx && usermod -d /home/nginx -s /bin/bash nginx
COPY requirements.txt /app/.
RUN  pip install -r requirements.txt
COPY . /app

#ASSIMP
WORKDIR /usr/local/assimp
RUN apt-get update -y
RUN apt-get update
RUN apt-get -y install cmake
RUN git clone https://github.com/assimp/assimp.git
WORKDIR /usr/local/assimp/assimp
RUN cmake CMakeLists.txt
RUN make -j4
RUN cp /usr/local/assimp/assimp/lib/libassimp.so /usr/local/lib

WORKDIR /app

ENTRYPOINT [ "python" ]
CMD ["run.py"]
