#!/bin/sh

hadoop fs -rm -r hw1_java

javac -d classes/ PatentStatistic.java && \
jar -cvf patentstatistic.jar -C classes/ ./ && \
hadoop jar patentstatistic.jar org.myorg.PatentStatistic /data/patents/apat63_99.txt hw1_java && \

hadoop fs -text ./hw1_java/part-r-00000 | head