#!/bin/sh

DIR=hw2_python/helper

hadoop fs -rm -r ${DIR}

hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -files mapperHelper.py,reducerHelper.py \
    -mapper mapperHelper.py \
    -reducer reducerHelper.py \
    -input /data/patents/cite75_99.txt \
    -output ${DIR} && \

hadoop fs -text ${DIR}/part-00000 | head
