FROM ubuntu:18.04
LABEL maintainer="someone <someone@gmail.com>"

# Docker must have at least CPU 2, Memory 8GiB

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
#RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    bash \
    git \
    emacs \
    python2.7 \
    dh-autoreconf \
    build-essential \
    unzip \
#    tzdata \
    libarchive-dev \
    r-base \
    ed 
#    wget

# Setup python
RUN cd /usr/bin/; ln -s python2.7 python
#RUN wget https://bootstrap.pypa.io/get-pip.py #-o get-pip.py
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python2.7 get-pip.py
RUN python2.7 -m pip install pandas==0.22

# Setup R
RUN R -e "install.packages('caret', repos = 'http://cran.us.r-project.org', dependencies = TRUE)"
RUN R -e "install.packages('randomForest', repos = 'http://cran.us.r-project.org', dependencies = TRUE)"
RUN R -e "install.packages('DBI', repos = 'http://cran.us.r-project.org', dependencies = TRUE)"

RUN git clone https://github.com/matthewdmanning/flood_data.git
RUN cd flood_data ; git checkout containers
RUN cd flood_data/repro; curl https://www.hydroshare.org/django_irods/download/bags/9e1b23607ac240588ba50d6b5b9a49b5.zip -o 9e1b23607ac240588ba50d6b5b9a49b5.zip
RUN cd flood_data/repro; unzip 9e1b23607ac240588ba50d6b5b9a49b5.zip
RUN cd flood_data/repro; mv 9e1b23607ac240588ba50d6b5b9a49b5/data/contents/hampt_rd_data.sqlite .

ENV PATH=/:$PATH

# === How to run
# docker run -it -v ${PWD}:/flood_data/repro/outfile waterbear:latest
