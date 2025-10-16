FROM python:3.11-bullseye AS spark-base

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      sudo \
      curl \
      vim \
      unzip \
      rsync \
      openjdk-17-jdk \
      build-essential \
      software-properties-common \
      ssh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

## Download spark and hadoop dependencies and install

# ENV variables
ENV SPARK_VERSION=4.0.0

ENV SPARK_HOME=${SPARK_HOME:-"/opt/spark"}
ENV HADOOP_HOME=${HADOOP_HOME:-"/opt/hadoop"}

ENV SPARK_MASTER_PORT=7077
ENV SPARK_MASTER_HOST=spark-master
ENV SPARK_MASTER="spark://$SPARK_MASTER_HOST:$SPARK_MASTER_PORT"

ENV PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
ENV PYSPARK_PYTHON=python3

# Add iceberg spark runtime jar to IJava classpath
ENV IJAVA_CLASSPATH=/opt/spark/jars/*

RUN mkdir -p ${HADOOP_HOME} && mkdir -p ${SPARK_HOME}
WORKDIR ${SPARK_HOME}

# Download spark
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
    && rm -f /tmp/${SPARK_TGZ_FILE}

# Add spark binaries to shell and enable execution
RUN chmod u+x /opt/spark/sbin/* && \
    chmod u+x /opt/spark/bin/*
ENV PATH="$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin"

# Add a spark config for all nodes
COPY conf/spark-defaults.conf "$SPARK_HOME/conf/"


FROM spark-base AS pyspark

# Install python deps
COPY requirements.txt .
RUN pip3 install -r requirements.txt


FROM pyspark AS pyspark-runner
ARG KAFKA_CLIENTS_VERSION=3.7.0
ARG SPARK_VERSION=4.0.0
ARG SCALA_VERSION=2.13
# Download iceberg spark runtime
RUN curl -L -# https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-4.0_2.13/1.10.0/iceberg-spark-runtime-4.0_2.13-1.10.0.jar -Lo /opt/spark/jars/iceberg-spark-runtime-4.0_2.13-1.10.0.jar

# Download delta jars (Scala 2.13 for Spark 4.0)
# Note: Delta Lake support for Spark 4.0 is experimental - these may not work perfectly
RUN curl -L -# https://repo1.maven.org/maven2/io/delta/delta-core_2.13/2.4.0/delta-core_2.13-2.4.0.jar -Lo /opt/spark/jars/delta-core_2.13-2.4.0.jar || echo "Delta core jar not found"
RUN curl -L -# https://repo1.maven.org/maven2/io/delta/delta-spark_2.13/3.2.0/delta-spark_2.13-3.2.0.jar -Lo /opt/spark/jars/delta-spark_2.13-3.2.0.jar || echo "Delta spark jar not found"
RUN curl -L -# https://repo1.maven.org/maven2/io/delta/delta-storage/3.2.0/delta-storage-3.2.0.jar -Lo /opt/spark/jars/delta-storage-3.2.0.jar || echo "Delta storage jar not found"

RUN curl -L -# https://jdbc.postgresql.org/download/postgresql-42.7.7.jar -Lo /opt/spark/jars/postgresql-42.7.7.jar || echo "postgresql-42.7.7.jar not found"
# Download hudi jars (Scala 2.13 for Spark 4.0) - experimental support
RUN curl -L -# https://repo1.maven.org/maven2/org/apache/hudi/hudi-spark3-bundle_2.13/0.15.0/hudi-spark3-bundle_2.13-0.15.0.jar -Lo /opt/spark/jars/hudi-spark3-bundle_2.13-0.15.0.jar || echo "Hudi jar not found"

# Download spark-sql-kafka-0-10_2.13
RUN curl -L -# https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.13/4.0.0/spark-sql-kafka-0-10_2.13-4.0.0.jar -Lo /opt/spark/jars/spark-sql-kafka-0-10_2.13-4.0.0.jar || echo "spark-sql-kafka"

RUN curl -L -# "https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/4.0.0/kafka-clients-4.0.0.jar" -Lo "/opt/spark/jars/kafka-clients-4.0.0.jar"

RUN curl -L -# "https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.13/4.0.0/spark-token-provider-kafka-0-10_2.13-4.0.0.jar" \
    -Lo "/opt/spark/jars/spark-token-provider-kafka-0-10_2.13-4.0.0.jar"

RUN curl -L -# "https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.12.0/commons-pool2-2.12.0.jar" \
    -o "/opt/spark/jars/commons-pool2-2.12.0.jar"
COPY entrypoint.sh /opt/spark/entrypoint.sh
RUN chmod u+x /opt/spark/entrypoint.sh


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