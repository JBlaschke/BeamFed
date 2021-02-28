#!/usr/bin/env python
# -*- coding: utf-8 -*-



from . import api
from . import DataRecord

from json import loads



def get_data_record(data_id):

    resp, _ = api.dataView(data_id)

    return DataRecord(
        resp.data[0].id,
        resp.data[0].title, resp.data[0].owner,
        loads(resp.data[0].metadata)
    )

