#!/usr/bin/env python
# -*- coding: utf-8 -*-



from . import api
from . import CollectionList, CollectionItem, DataRecordItem,\
              is_collection, is_collection_id, is_data_record, is_data_record_id

from . import STEP as protobuf_step



def collection_from_id(id):

    resp, _ = api.CollectionView(id)

    return CollectionItem(
        resp.coll[0].id,
        resp.coll[0].title, resp.coll[0].alias, resp.coll[0].owner
    )



def list_items(collection_name):

    collections = list()
    data_records = list()

    protobuf_offset = 0
    while True:
        resp, _ = api.collectionItemsList(
            collection_name, count=protobuf_step, offset=protobuf_offset
        )

        if resp.offset > resp.total:
            break


        for item in resp.item:
            if is_collection(item):
                collections.append(
                    CollectionItem(item.id, item.title, item.alias, item.owner)
                )

            if is_data_record(item):
                data_records.append(
                    DataRecordItem(item.id, item.title, item.owner)
                )

        protobuf_offset += protobuf_step

    return CollectionList(
        coll=collections,
        data=data_records
    )



def find_collection(name, parent="root"):

    root = list_items(parent)
    f    = filter(lambda x:x.title==name, root.coll)
    return list(f)



def traverse_find_collection(name, root="root"):

    coll = find_collection(name, parent=root)
    assert len(coll) <= 1

    if len(coll) > 0:
        return coll[0]

    for child in list_items(name).col:
        traverse_find_collection(name, parent=child)



def ensure_collection(name, parent, alias=None):

    if is_collection_id(name):
        coll = [collection_from_id(name)]
    else:
        coll = find_collection(name, parent=parent)

    assert len(coll) <= 1

    if len(coll) > 0:
       return coll[0]

    if alias is None:
        resp, _ = api.collectionCreate(name, parent_id=parent)
    else:
        resp, _ = api.collectionCreate(name, alias=alias, parent_id=parent)
    return CollectionItem(
        resp.coll[0].id,
        resp.coll[0].title, resp.coll[0].alias, resp.coll[0].owner
    )
