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
    """
    Basic transaction data as in Bitcoin, initialized to nonsense
    """
    def __init__(self, own_hash, prev_hash):
        self.meta_data = {'hash': own_hash,   # As in Bitcoin
                          'ver': -1,    # see https://en.bitcoin.it/wiki/Transaction
                          'vin_sz': -1,
                          'lock_time': -1,
                          'size':-1
                        }
        # Move this below to update_trans_data???
        self.in_data = {'hash': prev_hash,
                   'n': -1} # Dummy value
        self.out_data = {'value': -1, # Dummies for now
                    'scrip_pub_key': -1}


class StateMachine:
    """
    State machine class definition

    :param:
    :return:
    """
    import networkx as nx

    def __init__(self):
        # Time stamping
        self.time_stamp = self.hash_method(str(datetime.now())) #CHECK ON TIME ZONES!!!

        # Define initial graph structure based on state machine / work flow
        self.graph = self.init_graph()
        self.trans_data = TransData(-1, -1) # Initialize???

    def get_graph_dict(self):
        return str(nx.to_dict_of_dicts(self.graph))

    # def get_gml_str(self):
    #     """
    #     Returns concatented string encoding gml of graph
    #     :param gml:
    #     :return:
    #     """
    #     g_gml = nx.generate_gml(self.graph)
    #
    #     g_list = []
    #     try:
    #         while True:
    #             g_el = g_gml.next()
    #             g_list.append(g_el)
    #     except StopIteration:
    #         pass
    #
    #     g_string = '-'.join(g_list)
    #     return g_string

    def init_graph(self):
        G = nx.DiGraph()
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

    def state_hash_digest(self):
        """
        Hashes graph structure with ornamentation
        :return:
        """
        g_gml = nx.generate_gml(self.graph)
        #g_string = self.get_gml_str()
        g_string = self.get_graph_dict()
        #g_string = 'twas brillig'
        self.g_string = g_string

        g_hash = self.hash_method(g_string)
        self.g_hash = g_hash
        self.g_digest = g_hash.digest()
        return g_hash.digest()

    def state_digest(self):
        """
        Returns digest of hashed
        :return:
        """
        g_hash = self.g_hash
        return(g_hash.digest())

    def whole_hash(self):
        """Hash graph state and time stamp for unique instance identifier"""
        whole_hash = self.hash_method(self.time_stamp)
        #whole_hash = whole_hash.update(self.g_digest)
        self.whole_hash = whole_hash

    def whole_digest(self):
        return(self.whole_hash.digest())

    def update_node(self, node_name, sent_from, sent_to):
        """
        Encode next step in state machine by updating node decorations
        :param node_name:
        :param sent_from:
        :param sent_to:
        :return:
        """

        # Update graph
        self.graph[node_name]['from'] = sent_from
        self.graph[node_name]['to'] = sent_to

        # Calculate new state hash
        self.graph[node_name]['statehashdigest'] = self.state_hash_digest()
        #self.graph[node_name]['statehashdigest'] = 'frabjous'

    # Calculate new whole hash (graph plus time stamp)
        #self.whole_hash()
        #self.whole_digest()

        # Update transaction data
        #self.set_trans_data(node_name)

    def set_trans_data(self, node_name):
        """

        :param node_name:
        :return:
        """
        # Calculate state hash

        prev_node = self.graph.predecessors(node_name)
        # Ensure that single previous node, otherwise multiple previous hashes (accommodate this too???)
        if len(prev_node) == 1:
            self.trans_data = TransData(prev_node.meta_data.hash)
        else: raise ValueError('Non-unique previous nodes')

        # assign current state hash
        self.trans_data.meta_data.hash = self.whole_hash


class SimpleSM(StateMachine):
    """ Class definition for simplest state machine of thing-lending with insurance"""
    #def __init__(self): # Moved back to base class, no overwriting needed

    # Overwrite from base class
    def init_graph(self):
        G = nx.DiGraph()
        G.add_nodes_from(['initial', 'offered', 'interested', 'insured', 'transferred', 'returned'])
        G.add_edges_from([('initial', 'offered'),
                          ('offered', 'interested'),
                          ('offered', 'insured'),
                          ('interested', 'transferred'),
                          ('transferred', 'returned')
                          ])
        return(G)

