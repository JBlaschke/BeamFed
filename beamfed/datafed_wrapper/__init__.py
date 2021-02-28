#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from datafed.CommandLib import API
except ImportError:
    raise RuntimeError('DataFed not found.')


from datafed import version



api = API()
root_context = "p/mat003"

api.setContext(root_context)


from .verify      import *
from .protobuf    import *
from .collection  import *
from .data_record import *
from .task_list   import *
