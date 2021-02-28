#!/usr/bin/env python
# -*- coding: utf-8 -*-



from json    import load, dumps
from os      import mkdir
from os.path import join, exists

from . import df



def send(data_path, dest, name, metadata):

    resp, _ = df.api.dataCreate(
        name,
        metadata = dumps(metadata),
        parent_id = dest
    )

    resp, _ = df.api.dataPut(
        resp.data[0].id,
        data_path,
        wait = False
    )

    return resp


def get(src_id, data_dir):

    gets_resp, _ = df.api.dataGet(
        [src_id],
        data_dir,
        orig_fname = True,
        wait = False
    )



def sync(data_path, root=None):

    with open(join(data_path, "xfer.json"), "r") as f:
        xfer_descriptor = load(f)

    df_descriptor = xfer_descriptor["datafed"]
    if root is None:
        owner = df_descriptor["owner"]
    else:
        owner = root

    coll = df.ensure_collection(df_descriptor["collection"], owner)
    coll_ls = df.list_items(coll.id)

    for target in xfer_descriptor["targets"]:

        idlo, idhi       = xfer_descriptor["id_range"]
        daqlo, daqhi     = xfer_descriptor["daq_range"]
        chunklo, chunkhi = xfer_descriptor["chunk_range"]

        for id in range(idlo, idhi + 1):
            for daq in range(daqlo, daqhi + 1):
                for chunk in range(chunklo, chunkhi + 1):
                    file_name = target.format(id=id, daq=daq, chunk=chunk)
                    file_path = join(data_path, file_name)

                    file_local = exists(file_path)

                    remote_occur = list(
                        filter(lambda x:x.title == file_name, coll_ls.data)
                    )
                    assert len(remote_occur) <= 1
                    file_remote = len(remote_occur) > 0

                    if file_local and not file_remote:
                        metadata = {
                            "site": xfer_descriptor["site"],
                            "run": id,
                            "daq": daq,
                            "chunk": chunk,
                            "test": df_descriptor["test"]
                        }

                        send(file_path, coll.id, file_name, metadata)

                    if file_remote and not file_local:
                        get(remote_occur[0].id, data_path)

    for child in xfer_descriptor["children"]:

        dir_path = join(data_path, child)
        if not exists(dir_path):
            mkdir(dir_path)

        sync(dir_path, root=coll.id)



def peek_local(data_path, root=None):

    with open(join(data_path, "xfer.json"), "r") as f:
        xfer_descriptor = load(f)

    df_descriptor = xfer_descriptor["datafed"]
    if root is None:
        owner = df_descriptor["owner"]
    else:
        owner = root

    coll = df.find_collection(df_descriptor["collection"], owner)
    assert len(coll) == 1

    coll_ls = df.list_items(coll[0].id)
    task_ls = df.get_running()

    loc_status = dict()

    for target in xfer_descriptor["targets"]:

        idlo, idhi       = xfer_descriptor["id_range"]
        daqlo, daqhi     = xfer_descriptor["daq_range"]
        chunklo, chunkhi = xfer_descriptor["chunk_range"]

        for id in range(idlo, idhi + 1):
            for daq in range(daqlo, daqhi + 1):
                for chunk in range(chunklo, chunkhi + 1):
                    file_name = target.format(id=id, daq=daq, chunk=chunk)
                    file_path = join(data_path, file_name)

                    file_local = exists(file_path)

                    remote_occur = list(
                        filter(lambda x:x.title == file_name, coll_ls.data)
                    )
                    assert len(remote_occur) <= 1
                    file_remote = len(remote_occur) > 0

                    file_in_transit = False
                    if file_remote:
                        remote_id = remote_occur[0].id

                        task_occur = list(
                            filter(lambda x:(x.source == remote_id or x.dest == remote_id), task_ls)
                        )

                        file_in_transit = len(task_occur) > 0

                    if file_local or file_remote:
                        loc_status[file_path] = {
                            "collection": False,
                            "remote": file_remote,
                            "local": file_local,
                            "in_transit": file_in_transit
                        }


    children = xfer_descriptor["children"]
    for child in children:
        child_path = join(data_path, child)

        child_local = exists(child_path)

        remote_occur = list(
            filter(lambda x:x.title == child, coll_ls.coll)
        )
        assert len(remote_occur) <= 1

        child_remote = len(remote_occur) > 0

        if child_local or child_remote:
            loc_status[child_path] = {
                "collection": True,
                "remote": child_remote,
                "local": child_local,
                "in_transit": False
            }

    return loc_status



def peek_remote(coll_id):

    coll_ls = df.list_items(coll_id)
    task_ls = df.get_running()

    loc_status = dict()

    for remote_file in coll_ls.data:

        remote_data = df.get_data_record(remote_file.id)

        task_occur = list(
            filter(lambda x:(x.source == remote_file.id or x.dest == remote_file.id), task_ls)
        )
        file_in_transit = len(task_occur) > 0

        loc_status[remote_file.id] = {
            "collection": False,
            "name": remote_file.title,
            "metadata": remote_data.metadata,
            "in_transit": file_in_transit
        }

    for remote_collection in coll_ls.coll:

        loc_status[remote_collection.id] = {
            "collection": True,
            "name": remote_collection.title
        }

    return loc_status
