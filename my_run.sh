#!/bin/sh

hadoop fs -rm -r my_output

hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -file my_mapper.py my_reducer.py \
    -mapper 'my_mapper.py 1 4' \
    -reducer my_reducer.py \
    -input /data/patents/apat63_99.txt \
    -output my_output
