Usage:

Specify one of encodings in the command line: VarByte or Simple9

1. Run map-reduce on cluster:
    ./runHadoop.sh Simple9

2. Build index on local computer:
    ./runBuildingIndex.sh Simple9

3. Search sites:
    ./run.sh Simple9
    >> маринованные AND огурцы AND NOT грибы OR картошка
    >> NOT борщ AND сметана
    >> кровавая OR мэри
    >> Ctrl-D