#!/usr/bin/env python
# -*- coding: utf-8 -*-



from typing      import List, Dict, Any
from dataclasses import dataclass



STEP = 100


@dataclass
class CollectionItem:
    id: str
    title: str
    alias: str
    owner: str



@dataclass
class DataRecordItem:
    id: str
    title: str
    owner: str



@dataclass
class DataRecord:
    id: str
    title: str
    owner: str
    metadata: Dict[str, Any]



@dataclass
class CollectionList:
    coll: List[CollectionItem]
    data: List[DataRecordItem]



@dataclass
class Task:
    id: str
    msg: str
    type: int
    source: str
    dest: str



def is_collection(item):
    return is_collection_id(item.id)



def is_collection_id(id):
    return id[:2] == "c/"



def is_data_record(item):
    return is_data_record_id(item.id)



def is_data_record_id(id):
    return id[:2] == "d/"
