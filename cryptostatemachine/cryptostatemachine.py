#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class definitions for the package cryptostatemachine, a Python implementation
of state machines with time-stamps and a cryptographic audit trail
"""
from __future__ import division, print_function, absolute_import

import argparse
import sys
import logging

import networkx as nx
import hashlib as hl
import

from cryptostatemachine import __version__

__author__ = "rastapavel"
__copyright__ = "rastapavel"
__license__ = "none"

_logger = logging.getLogger(__name__)


class StateMachine:
    """
    State machine class definition

    :param n: integer
    :return: n-th Fibonacci number
    """
    def __init__(self):
        self.graph = nx.graph()

    def graph_digest(self):
        g_gml = nx.generate_gml(self.graph)
        g_list = []
        for i in range(0,3):
            g_list.append(g_gml.next())
        g_string = '-'.join(g_list)
        g_hash = hl.sha256(g_string)
        self.g_digest = g_hash.digest()
        return(self.g_digest)
