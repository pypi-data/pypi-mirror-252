# -*- coding: utf-8 -*-

"""
    Database Connector
    ~~~

    Database connector for different DBs with same interface.

    :copyright: (c) 2023 by Stepan Starovoitov.
    :license: BSD, see LICENSE for more details.
"""
__version__ = "0.1.1"

from dbcc.base import TableEngine
from dbcc.mongodb import MongoTableEngine
