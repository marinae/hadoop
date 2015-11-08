#!/bin/sh

SITE=povarenok.ru
SIZE=all
MAPPER=mapper.py
REDUCER=reducer.py
INPUT=$(hadoop fs -ls /data/sites/${SITE}/all/docs-*.txt | awk '{print $NF}' | tr '\n' ',' | rev | cut -c 2- | rev)
echo $INPUT
OUTPUT_DIR=index
ENCODER=encoder.zip
BS_DIR=bs4.zip

if [[ "$1" != "VarByte" ]] && [[ "$1" != "Simple9" ]]; then
    echo "Please specify one of encodings: VarByte or Simple9"
    exit
fi

rm -f part-00000 && \
hadoop fs -rm -f -r ${OUTPUT_DIR} && \

hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -files ${MAPPER},${REDUCER},${ENCODER},${BS_DIR} \
    -mapper ${MAPPER} \
    -reducer "${REDUCER} $1" \
    -input ${INPUT} \
    -output ${OUTPUT_DIR} && \

hadoop fs -text ${OUTPUT_DIR}/part-00000 | head && \
hadoop fs -get ${OUTPUT_DIR}/part-00000
