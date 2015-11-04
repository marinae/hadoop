#!/bin/sh

SITE=povarenok.ru
SIZE=1_1000
MAPPER=mapper.py
REDUCER=reducer.py
INPUT=/data/sites/${SITE}/${SIZE}/docs-000.txt
OUTPUT_DIR=index
BS_DIR=bs4.zip

rm -f part-00000 && \
hadoop fs -rm -f -r ${OUTPUT_DIR} && \

hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -files ${MAPPER},${REDUCER},${BS_DIR} \
    -mapper ${MAPPER} \
    -reducer "${REDUCER} $1" \
    -input ${INPUT} \
    -output ${OUTPUT_DIR} && \

hadoop fs -text ${OUTPUT_DIR}/part-00000 | head && \
hadoop fs -get ${OUTPUT_DIR}/part-00000
