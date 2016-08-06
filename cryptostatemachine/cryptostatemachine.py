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
from collections import namedtuple as nt

from cryptostatemachine import __version__

__author__ = "rastapavel"
__copyright__ = "rastapavel"
__license__ = "none"

_logger = logging.getLogger(__name__)

class TransData():
    def __init__(self):
        self.meta_data = {'hash': -1, # As in Bitcoin
                          'ver': -1,
                          'vin_sz': -1,
                          'lock_time': -1,
                          'size':-1
                        }
        self.in_data = self.set_inout_data(-1, -1)
        self.out_data = self.set_inout_data(-1, -1)

    def set_inout_data(self, prev_hash, prev_n):
        inout_data = {'hash': prev_hash,
                   'n': prev_n}
        return(inout_data)

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
        self.time_stamp = self.hash_method(str(datetime.now())) #CHECK ON TIME ZONES!!!
        #self.time_stamp = t_hash.hexdigest()
        # Define initial graph structure based on state machine / work flow
        self.graph = self.init_graph()
        self.trans_data = TransData()

    def init_graph(self):
        G = nx.Graph()
        G.add_node("initial")
        return(G)

    def hash_method(self, to_hash):
        """
        Define hash function of choice for class

        :param: thing to hash
        :return: hash of thing, with chosen hash method for experimenting
        """
        my_hash = hl.sha256(to_hash)
        #my_hash = hl.sha1(to_hash)
        return(my_hash)

    def state_hash(self):
        """
        Hashes graph structure with ornamentation
        :return:
        """
        g_gml = nx.generate_gml(self.graph)
        g_list = []
        for i in range(0,3):
            g_list.append(g_gml.next())
        g_string = '-'.join(g_list)
        #g_hash = hl.sha256(g_string)
        self.g_hash = self.hash_method(g_string)

    def state_digest(self):
        """
        Returns digest of hashed
        :return:
        """
        return(self.g_hash.digest())

    def whole_hash(self):
        """Hash graph state and time stamp for unique instance identifier"""
        whole_hash = self.hash_method(self.time_stamp)
        whole_hash = whole_hash.update(self.g_digest)
        self.whole_hash = whole_hash

    def whole_digest(self):
        return(self.whole_hash.digest())

class SimpleSM(StateMachine):
    """ Class definition for simplest state machine of thing-lending with insurance"""
    #def __init__(self): # Moved back to base class, no overwriting needed

    # Overwrite from base class
    def init_graph(self):
        G = nx.Graph()
        G.add_nodes_from(['initial', 'offered', 'interested', 'insured', 'transferred', 'returned'])
        G.add_edges_from([('initial', 'offered'),
                          ('offered', 'interested'),
                          ('offered', 'insured'),
                          ('interested', 'transferred'),
                          ('transferred', 'returned')
                          ])
        return(G)