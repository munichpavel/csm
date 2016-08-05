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
from datetime import datetime, timedelta # Get up to microseconds
import bitcoin as bc

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
        # Time stamping
        #t_hash = hl.sha256()
        #t_hash.update(str(datetime.now())) #CHECK ON TIME ZONES!!!
        t_hash = self.sm_hash(str(datetime.now())) #CHECK ON TIME ZONES!!!
        self.time_stamp = t_hash.hexdigest()[0:64]
        # Define initial graph structure based on state machine / work flow
        self.graph = self.init_graph()

    def init_graph(self):
        G = nx.Graph()
        G.add_node("initial")
        return(G)

    def sm_hash(self, to_hash):
        """
        Define hash function of choice for class

        :param: thing to hash
        :return: hash of thing, with chosen hash method for experimenting
        """
        my_hash = hl.sha256(to_hash)
        #my_hash = hl.sha1(to_hash)
        return(my_hash)

    def state_digest(self):
        g_gml = nx.generate_gml(self.graph)
        g_list = []
        for i in range(0,3):
            g_list.append(g_gml.next())
        g_string = '-'.join(g_list)
        #g_hash = hl.sha256(g_string)
        g_hash = self.sm_hash(g_string)
        self.g_digest = g_hash.digest()
        return(self.g_digest)

    def state_hash(self):
        """Hash graph state and time stamp for unique instance identifier"""

class SimpleSM(StateMachine):
    """ Class definition for simplest state machine of thing-lending with insurance"""
    #def __init__(self): # Moved back to base class, no overwriting needed

    # Overwrite from base class
    def init_graph(self):
        G = nx.Graph()
        G.add_nodes_from(['initial', 'offered', 'accepted', 'insured', 'returned'])
        G.add_edges_from([('initial', 'offered'), ('offered', 'accepted'),('offered', 'insured'), ('accepted', 'returned')])
        return(G)