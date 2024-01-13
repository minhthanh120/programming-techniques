# 
FROM spark:3.5.0-scala2.12-java11-ubuntu

USER root

RUN set -ex; \
    apt-get update; \
    apt-get install -y python3 python3-pip; \
    apt-get install -y r-base r-base-dev; \
    rm -rf /var/lib/apt/lists/*

ENV R_HOME /usr/lib/R

# 
WORKDIR /tmp

# 
COPY ./requirements.txt /tmp/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

RUN useradd -r -s /bin/false jovyan

USER jovyan
# 
WORKDIR /home/jovyan

#COPY ./app /code/app
#
#WORKDIR /code/app
# 
#CMD ["jupyter", "notebook", "--no-browser", "--port", "8001"]
