#!/usr/bin/env python
# -*- coding: utf-8 -*-



from . import api
from . import Task



TS_RUNNING = 2



def get_running(status=[TS_RUNNING], count=100):
    task_list, _ = api.taskList(status=status, count=count)

    return [
        Task(task.id, task.msg, task.type, task.source, task.dest)
        for task in task_list.task
    ]
