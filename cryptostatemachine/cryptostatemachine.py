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

import json


from cryptostatemachine import __version__

__author__ = "rastapavel"
__copyright__ = "rastapavel"
__license__ = "none"

_logger = logging.getLogger(__name__)

class TransData():
    """
    Basic transaction data as in Bitcoin, initialized to nonsense
    TODO: Check against Segregated Witness BIP 141
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

    def export_as_dict(self):
        """

        :return: TransData as dictionary of dictionaries
        """
        self.trans_dict = {"meta_data": self.meta_data,
                      "in_data": self.in_data,
                      "out_data": self.out_data}
        return(self.trans_dict)


class StateMachine:
    """
    State machine class definition

    :param:
    :return:
    """
    import networkx as nx

    def __init__(self):
        # Time stamping
        self.time_stamp = self.hash_method(str(datetime.now())).hexdigest() #CHECK ON TIME ZONES!!!

        # Define initial graph structure based on state machine / work flow
        self.graph = self.init_graph()
        self.set_graph_digest()
        self.graph['initial']['statehashdigest'] = self.set_whole_digest()
        self.trans_data = TransData(self.whole_digest, -1) # Initialize???

    def get_graph_str(self):
        return str(nx.to_dict_of_dicts(self.graph))

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

    def set_graph_digest(self):
        """
        Hashes graph structure with ornamentation
        :return:
        """
        g_gml = nx.generate_gml(self.graph)
        #g_string = self.get_gml_str()
        g_string = self.get_graph_str()
        #g_string = 'twas brillig'
        self.g_string = g_string

        g_hash = self.hash_method(g_string)
        self.g_hash = g_hash                # Move these onto nodes attributes?
        self.g_digest = g_hash.hexdigest()     # Move these node attributes?
        return g_hash.hexdigest()


    def set_whole_digest(self):
        """
        Hash graph state and time stamp for unique instance identifier
        Only called from within update_node

        """

        whole_hash = self.hash_method(self.time_stamp + self.g_digest) # TODO: Is this a good idea?
        #whole_hash_digest = whole_hash.hexdigest()
        self.whole_hash = whole_hash
        self.whole_digest = whole_hash.hexdigest()
        return(self.whole_digest)

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

        # Update graph hash
        self.set_graph_digest()

        # Calculate new whole hash
        self.graph[node_name]['statehashdigest'] = self.set_whole_digest()

        # Update transaction data
        self.set_trans_data(node_name)

    def set_trans_data(self, node_name):
        """

        :param node_name:
        :return:
        """
        # Calculate state hash

        prev_node = self.graph.predecessors(node_name)
        # Ensure that single previous node, otherwise multiple previous hashes (accommodate this too???)
        if len(prev_node) == 1:
            pass
            self.trans_data = TransData(self.whole_digest, self.graph[prev_node[0]]['statehashdigest'])
        else: raise ValueError('Non-unique previous nodes')

    def write_trans_data(self, file):
        """

        :param file:
        :return:
        """
        with open(file, 'w') as outfile:
            json.dump(self.trans_data.export_as_dict(), outfile)

class SimpleSM(StateMachine):
    """ Class definition for simplest state machine of thing-lending with insurance"""

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

