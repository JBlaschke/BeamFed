#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sys     import argv
from os.path import join
from json    import load

from .       import df
from .files  import sync, peek_local, peek_remote



def status_str(file_local, file_remote, in_tranist):

    descr_str = "("

    delim = lambda x: "," if x[-1] != "(" else ""

    if file_local:
        descr_str += "L"

    if file_remote:
        descr_str += delim(descr_str) + "R"

    if in_tranist:
        descr_str += delim(descr_str) + "T"

    descr_str += ")"

    return descr_str



def run():

    if argv[1] == "verify":
        df_status = df.verify()
        print(df_status)


    if argv[1] == "ls":
        df_ls = df.list_items(argv[2])
        print(df_ls)


    if argv[1] == "lsl":
        ls_local = peek_local(argv[2])

        print("")
        print("Local FILES:")
        print("------------")

        for key, status in ls_local.items():
            if not status["collection"]:
                sstr = status_str(
                    status["local"], status["remote"], status["in_transit"]
                )
                print(f"{key:<80} {sstr}")

        print("")
        print("Local FOLDERS:")
        print("------------")

        for key, status in ls_local.items():
            if status["collection"]:
                sstr = status_str(
                    status["local"], status["remote"], status["in_transit"]
                )
                print(f"{key:<80} {sstr}")


    if argv[1] == "lsr":
        ls_local = peek_remote(argv[2])

        print("")
        print("Remote DATA RECORDS:")
        print("------------")

        for key, status in ls_local.items():
            if not status["collection"]:
                name = status["name"]
                metadata = status["metadata"]
                if status["in_transit"]:
                    print(f"{key:<12} (T) {name:<16} {metadata}")
                else:
                    print(f"{key:<16} {name:<16} {metadata}")

        print("")
        print("Remote COLLECTIONS:")
        print("------------")

        for key, status in ls_local.items():
            if status["collection"]:
                name = status["name"]
                print(f"{key:<12} {name:<16}")

    if argv[1] == "mk":

        with open(join(argv[2], "xfer.json"), "r") as f:
            xfer_descriptor = load(f)

        df_descriptor = xfer_descriptor["datafed"]
        owner = df_descriptor["owner"]

        coll = df.ensure_collection(df_descriptor["collection"], owner)


    if argv[1] == "id":
        if len(argv) > 3:
            coll_id = df.find_collection(argv[2], parent=argv[3])
            print(coll_id)
        else:
            coll_id = df.find_collection(argv[2])
            print(coll_id)


    if argv[1] == "sync":
        sync(argv[2])



if __name__ == "__main__":
    run()
