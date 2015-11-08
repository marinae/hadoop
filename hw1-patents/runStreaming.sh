#!/bin/sh

hadoop fs -rm -r hw1_python

hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -files mapper.py,reducer.py \
    -mapper 'mapper.py 1 4' \
    -reducer reducer.py \
    -input /data/patents/apat63_99.txt \
    -output hw1_python && \

hadoop fs -text ./hw1_python/part-00000 | head
