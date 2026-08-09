#!/bin/bash
set -e

SPARK_WORKLOAD="$1"

echo "SPARK_WORKLOAD: $SPARK_WORKLOAD"

case "$SPARK_WORKLOAD" in

  master|*/start-master.sh)
    exec /opt/spark/sbin/start-master.sh -p 7077
    ;;

  worker|*/start-worker.sh)
    exec /opt/spark/sbin/start-worker.sh spark://spark-master:7077
    ;;

  history|*/start-history-server.sh)
    exec /opt/spark/sbin/start-history-server.sh
    ;;

  *)
    echo "Unknown SPARK_WORKLOAD: $SPARK_WORKLOAD"
    echo "Expected:"
    echo "  master"
    echo "  worker"
    echo "  history"
    echo "  /opt/spark/sbin/start-master.sh"
    echo "  /opt/spark/sbin/start-worker.sh"
    echo "  /opt/spark/sbin/start-history-server.sh"
    exit 1
    ;;

esac