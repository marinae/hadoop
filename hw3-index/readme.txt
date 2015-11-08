Usage:

1. Run map-reduce on cluster:
    a) ./runHadoop.sh VarByte
    b) ./runHadoop.sh Simple9

2. Build index on local computer:
    a) ./runBuildingIndex.sh VarByte
    b) ./runBuildingIndex.sh Simple9

3. Search sites:
    python query.py
    >> маринованные AND огурцы AND NOT грибы OR картошка
    >> NOT борщ AND сметана
    >> кровавая OR мэри
    >> Ctrl-D