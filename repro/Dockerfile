FROM ubuntu:18.04
LABEL maintainer="someone <someone@gmail.com>"
# Docker must have at least CPU 2, Memory 8GiB

RUN apt-get update

# ===== Setup R
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    r-base
RUN R -e "install.packages('caret', repos = 'http://cran.us.r-project.org', dependencies = TRUE)"
RUN R -e "install.packages('randomForest', repos = 'http://cran.us.r-project.org', dependencies = TRUE)"
RUN R -e "install.packages('DBI', repos = 'http://cran.us.r-project.org', dependencies = TRUE)"

# # ===== Other basic
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
     git \
     emacs \
#     dh-autoreconf \
#     build-essential \
     unzip 
#     libarchive-dev
     
# # ===== Python2.7 
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
     python2.7 \
     python-pip \
     python-pandas \
     python-matplotlib
    
# Setup python
#RUN cd /usr/bin/; ln -s python2.7 python
#RUN python2.7 -m pip install pandas==0.22

# ===== Git Repo
RUN git clone https://github.com/matthewdmanning/flood_data.git
RUN cd flood_data ; git checkout containers
RUN cd flood_data/repro; curl https://www.hydroshare.org/django_irods/download/bags/9e1b23607ac240588ba50d6b5b9a49b5.zip -o 9e1b23607ac240588ba50d6b5b9a49b5.zip
RUN cd flood_data/repro; unzip 9e1b23607ac240588ba50d6b5b9a49b5.zip
RUN cd flood_data/repro; mv 9e1b23607ac240588ba50d6b5b9a49b5/data/contents/hampt_rd_data.sqlite .

ENV PATH=/:$PATH

# === How to run
# docker run -it -v ${PWD}:/data/ waterbear:latest
# docker run -v ${PWD}:/data/ waterbear:latest /data/script.sh
