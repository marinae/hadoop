#!/bin/sh

DIR=hw2_java/helper

hadoop fs -rm -r ${DIR}

rm -r classes
mkdir classes && \

javac -d classes/ PageRankHelper.java && \
jar -cvf pagerankhelper.jar -C classes/ ./ && \
hadoop jar pagerankhelper.jar org.myorg.PageRankHelper /data/patents/cite75_99.txt ${DIR} && \

hadoop fs -text ${DIR}/part-r-00000 | head