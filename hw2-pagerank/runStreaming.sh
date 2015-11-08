#!/bin/sh

INPUT_FILE=hw2_python/helper/part-00000
WORK_DIR=hw2_python/pagerank
TEMP_DIR=hw2_python/pagerank_tmp

hadoop fs -rm -r ${WORK_DIR}
hadoop fs -rm -r ${TEMP_DIR}

hadoop fs -mkdir ${WORK_DIR} && \
hadoop fs -cp ${INPUT_FILE} ${WORK_DIR}/part-00000 && \

for i in $(seq 1 30); do

    echo "******************** Iteration $i ********************"

    hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -files mapper.py,reducer.py \
        -mapper mapper.py \
        -reducer reducer.py \
        -input ${WORK_DIR}/part-00000 \
        -output ${TEMP_DIR} && \

    hadoop fs -rm ${WORK_DIR}/part-00000 && \
    hadoop fs -mv ${TEMP_DIR}/part-00000 ${WORK_DIR}/part-00000 && \
    hadoop fs -rm -r ${TEMP_DIR} && \

    hadoop fs -text ${WORK_DIR}/part-00000 | sort -k2,2nr | head

done
