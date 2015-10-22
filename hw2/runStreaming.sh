#!/bin/sh

hadoop fs -rm -r page_rank_python
hadoop fs -rm -r page_rank_python_tmp

hadoop fs -mkdir page_rank_python && \
hadoop fs -cp ./page_rank_python_helper/part-00000 ./page_rank_python/part-00000 && \

for i in $(seq 1 20); do

    hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -files mapper_1.py,reducer_1.py \
        -mapper mapper_1.py \
        -reducer reducer_1.py \
        -input ./page_rank_python/part-00000 \
        -output page_rank_python_tmp

    hadoop fs -rm -r page_rank_python && \

    hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -files mapper_2.py,reducer_2.py \
        -mapper mapper_2.py \
        -reducer reducer_2.py \
        -input ./page_rank_python_tmp/part-00000 \
        -output page_rank_python

    hadoop fs -text ./page_rank_python/part-00000 | head

    hadoop fs -rm -r page_rank_python_tmp

done
