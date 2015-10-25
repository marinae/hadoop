#!/bin/sh

INPUT_FILE=hw2_java/helper/part-r-00000
WORK_DIR=hw2_java/pagerank
TEMP_DIR=hw2_java/pagerank_tmp

hadoop fs -rm -r ${WORK_DIR}

javac -d classes/ PageRank.java && \
jar -cvf pagerank.jar -C classes/ ./ && \
hadoop fs -mkdir ${WORK_DIR} && \
hadoop fs -cp ${INPUT_FILE} ${WORK_DIR}/part-r-00000 && \
hadoop jar pagerank.jar org.myorg.PageRank ${WORK_DIR} ${TEMP_DIR} && \

hadoop fs -text ${WORK_DIR}/part-r-00000 | sort -k2,2nr | head

hadoop fs -rm -r ${TEMP_DIR}