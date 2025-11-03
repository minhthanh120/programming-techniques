FROM python:3.11-slim-bullseye AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      sudo \
      curl \
      unzip \
      rsync \
      openjdk-17-jre-headless \
      ssh \
      build-essential \
      software-properties-common && \
    rm -rf /var/lib/apt/lists/*

# ENV variables
ENV SPARK_VERSION=4.0.0
ENV SPARK_HOME="/opt/spark"
ENV PATH="$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH"
ENV PYSPARK_PYTHON=python3
ENV PYTHONPATH="$SPARK_HOME/python/:$PYTHONPATH"

## Download spark and hadoop dependencies and install
# see resources: https://dlcdn.apache.org/spark/spark-4.0./
# filename: spark-4.0.0-bin-hadoop3.tgz

#RUN mkdir -p ${SPARK_HOME} \
#    && curl -L -# https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz -o spark-${SPARK_VERSION}-bin-hadoop3.tgz \
#    && tar xvzf spark-${SPARK_VERSION}-bin-hadoop3.tgz --directory ${SPARK_HOME} --strip-components 1 \
#    && rm -rf spark-${SPARK_VERSION}-bin-hadoop3.tgz

ARG SPARK_TGZ_FILE=spark-4.0.0-bin-hadoop3-connect.tgz

COPY ${SPARK_TGZ_FILE} /tmp/${SPARK_TGZ_FILE}

RUN mkdir -p ${SPARK_HOME} \
    && tar xvzf /tmp/${SPARK_TGZ_FILE} --directory ${SPARK_HOME} --strip-components 1 \
    && rm -f /tmp/${SPARK_TGZ_FILE}\
  && rm -rf /opt/spark/examples /opt/spark/data /opt/spark/kubernetes /opt/spark/yarn
# --- Install python packages ---
# Using virtual environment for isolate and easy to move
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Install jars ---
WORKDIR /opt/spark/jars
RUN curl -L -# https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-4.0_2.13/1.10.0/iceberg-spark-runtime-4.0_2.13-1.10.0.jar -o iceberg-spark-runtime-4.0_2.13-1.10.0.jar && \
    curl -L -# https://repo1.maven.org/maven2/io/delta/delta-core_2.13/2.4.0/delta-core_2.13-2.4.0.jar -o delta-core_2.13-2.4.0.jar && \
    curl -L -# https://repo1.maven.org/maven2/io/delta/delta-spark_2.13/3.2.0/delta-spark_2.13-3.2.0.jar -o delta-spark_2.13-3.2.0.jar && \
    curl -L -# https://repo1.maven.org/maven2/io/delta/delta-storage/3.2.0/delta-storage-3.2.0.jar -o delta-storage-3.2.0.jar && \
    curl -L -# https://jdbc.postgresql.org/download/postgresql-42.7.7.jar -o postgresql-42.7.7.jar && \
    curl -L -# https://repo1.maven.org/maven2/org/apache/hudi/hudi-spark3-bundle_2.13/0.15.0/hudi-spark3-bundle_2.13-0.15.0.jar -o hudi-spark3-bundle_2.13-0.15.0.jar && \
    curl -L -# https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.13/4.0.0/spark-sql-kafka-0-10_2.13-4.0.0.jar -o spark-sql-kafka-0-10_2.13-4.0.0.jar && \
    curl -L -# https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/4.0.0/kafka-clients-4.0.0.jar -o kafka-clients-4.0.0.jar && \
    curl -L -# https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.13/4.0.0/spark-token-provider-kafka-0-10_2.13-4.0.0.jar -o spark-token-provider-kafka-0-10_2.13-4.0.0.jar && \
    curl -L -# https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.12.0/commons-pool2-2.12.0.jar -o commons-pool2-2.12.0.jar

WORKDIR /

# =========================================================================
FROM python:3.11-slim-bullseye AS final-runner

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      sudo \
      curl \
      openjdk-17-jre-headless \
      ssh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV SPARK_HOME="/opt/spark"
ENV PATH="$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH"
ENV PYSPARK_PYTHON=python3
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --from=builder ${SPARK_HOME} ${SPARK_HOME}

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Add a spark config for all nodes
COPY conf/spark-defaults.conf "$SPARK_HOME/conf/"
COPY entrypoint.sh /opt/spark/entrypoint.sh
# Add spark binaries to shell and enable execution
RUN chmod u+x /opt/spark/entrypoint.sh && \
    chmod u+x /opt/spark/sbin/* && \
    chmod u+x /opt/spark/bin/*
# Optionally install Jupyter
# FROM pyspark-runner AS pyspark-jupyter

# RUN pip3 install notebook

# ENV JUPYTER_PORT=8889

# ENV PYSPARK_DRIVER_PYTHON=jupyter
# ENV PYSPARK_DRIVER_PYTHON_OPTS="notebook --no-browser --allow-root --ip=0.0.0.0 --port=${JUPYTER_PORT}"
# # --ip=0.0.0.0 - listen all interfaces
# # --port=${JUPYTER_PORT} - listen ip on port 8889
# # --allow-root - to run Jupyter in this container by root user. It is adviced to change the user to non-root.


ENTRYPOINT ["./entrypoint.sh"]
CMD [ "bash" ]

# Now go to interactive shell mode
# -$ docker exec -it spark-master /bin/bash
# then execute
# -$ pyspark

# If Jupyter is installed, you will see an URL: `http://127.0.0.1:8889/?token=...`
# This will open Jupyter web UI in your host machine browser.
# Then go to /warehouse/ and test the installation.