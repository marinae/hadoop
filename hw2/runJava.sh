#!/bin/sh

hadoop fs -rm -r page_rank

javac -d classes/ PageRank.java && \
jar -cvf pagerank.jar -C classes/ ./ && \
hadoop fs -mkdir page_rank && \
hadoop fs -cp ./page_rank_helper/part-r-00000 ./page_rank/part-r-00000 && \
hadoop jar pagerank.jar org.myorg.PageRank && \
hadoop fs -text ./page_rank/part-r-00000 | head

hadoop fs -rm -r page_rank_tmp