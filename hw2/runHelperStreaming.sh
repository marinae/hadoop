#!/bin/sh

hadoop fs -rm -r page_rank_python_helper

hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -files mapperHelper.py,reducerHelper.py \
    -mapper mapperHelper.py \
    -reducer reducerHelper.py \
    -input /data/patents/cite75_99.txt \
    -output page_rank_python_helper && \

hadoop fs -text ./page_rank_python_helper/part-00000 | head
