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

from cryptostatemachine import __version__

__author__ = "rastapavel"
__copyright__ = "rastapavel"
__license__ = "none"

_logger = logging.getLogger(__name__)


class StateMachine:
    """
    State machine class definition

    :param:
    :return:
    """
    import networkx as nx

    def __init__(self):
        G = nx.Graph()
        G.add_node("initial")
        self.graph = G


    def state_digest(self):
        g_gml = nx.generate_gml(self.graph)
        g_list = []
        for i in range(0,3):
            g_list.append(g_gml.next())
        g_string = '-'.join(g_list)
        g_hash = hl.sha256(g_string)
        self.g_digest = g_hash.digest()
        return(self.g_digest)

#    def __add_sender__(self, node):

class SimpleFlow(StateMachine):
    """ Class definition for simplest state machine of thing-lending with insurance"""
    def __init__(self):
        G = nx.Graph()
        G.add_nodes_from(['initial', 'offered', 'accepted', 'insured', 'returned'])
        G.add_edges_from([('initial', 'offered'), ('offered', 'accepted'),('offered', 'insured'), ('accepted', 'returned')])
        self.graph = G