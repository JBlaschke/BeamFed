#!/usr/bin/env python
# -*- coding: utf-8 -*-



from . import api, version



def verify():

    status = dict();

    status["version"] = version

    if api.getAuthUser():
        status["user_authorized"] = True
    else:
        status["user_authorized"] = False

    if api.endpointDefaultGet():
        status["has_endpoint"]     = True
        status["default_endpoint"] = api.endpointDefaultGet()
    else:
        status["has_endpoint"]     = True
        status["default_endpoint"] = None


    return status
