#!/bin/sh

hadoop fs -rm -r page_rank_helper

javac -d classes/ PageRankHelper.java && \
jar -cvf pagerankhelper.jar -C classes/ ./ && \
hadoop jar pagerankhelper.jar org.myorg.PageRankHelper /data/patents/cite75_99.txt page_rank_helper && \
hadoop fs -text ./page_rank_helper/part-r-00000 | head