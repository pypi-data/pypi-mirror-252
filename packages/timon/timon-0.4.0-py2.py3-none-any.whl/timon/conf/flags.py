#!/usr/bin/env python

# #############################################################################
# Copyright : (C) 2023 by MHComm. All rights reserved
#
# __author__ = "Quentin Laymajoux"
# __email__ = "info@mhcomm.fr"
#
# Name       : timon.conf.flags
"""
Summary: some flags used for example as probe results
"""
# #############################################################################

FLAG_OK = 0
FLAG_WARNING = 1
FLAG_ERROR = 2
FLAG_UNKNOWN = 3

FLAG_OK_STR = "OK"
FLAG_WARNING_STR = "WARNING"
FLAG_ERROR_STR = "ERROR"
FLAG_UNKNOWN_STR = "UNKNOWN"


FLAG_MAP = {
    FLAG_OK_STR: FLAG_OK,
    FLAG_WARNING_STR: FLAG_WARNING,
    FLAG_ERROR_STR: FLAG_ERROR,
    FLAG_UNKNOWN_STR: FLAG_UNKNOWN,
    }

INV_FLAG_MAP = {v: k for k, v in FLAG_MAP.items()}
