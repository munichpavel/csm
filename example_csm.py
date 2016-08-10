import os
import sys
import ecdsa as ec #Pure Python elliptic curve cryptography
import binascii as ba

import cryptostatemachine.cryptostatemachine as csm
reload(csm)

# Issuer
alice_priv = ec.SigningKey.generate()
alice_priv_hex = ba.b2a_hex(alice_priv.to_string())
alice_pub = alice_priv.get_verifying_key()
alice_pub_hex = ba.b2a_hex(alice_pub.to_string())
print 'Alice\'s public key:', alice_pub_hex, '\n'

# Interested party
bob_priv = ec.SigningKey.generate()
bob_priv_hex = ba.b2a_hex(bob_priv.to_string())
bob_pub = bob_priv.get_verifying_key()
bob_pub_hex = ba.b2a_hex(bob_pub.to_string())
print 'Bob\'s public key:', bob_pub_hex, '\n'

# Microinsurer
az_priv = ec.SigningKey.generate()
az_priv_hex = ba.b2a_hex(az_priv.to_string())
az_pub = az_priv.get_verifying_key()
az_pub_hex = ba.b2a_hex(az_pub.to_string())
print 'AZ public key:', az_pub_hex, '\n'

# P2P platform
p2p_priv = ec.SigningKey.generate()
p2p_priv_hex = ba.b2a_hex(p2p_priv.to_string())
p2p_pub = p2p_priv.get_verifying_key()
p2p_pub_hex = ba.b2a_hex(p2p_pub.to_string())
#print 'P2P public key:', p2p_pub

# JSON file to hold transaction data for blockchain (mock-up)
db_file = 'p2pthing.json' # Output file for transaction data

# Post offer of camera on P2P platform, back-end creates instance of SimpleSM
p2p_message = 'It looks like Alice wants to post a camera on our platform'
p2p_msg_signed = ba.b2a_hex(p2p_priv.sign(p2p_message))
ssm = csm.SimpleSM(p2p_pub_hex, p2p_msg_signed) # Initialize, and track which p2p platform is calling

# Initial graph

print 'Initial Graph Nodes: \n', ssm.graph.nodes(), '\n'

print 'Initial Graph Edges: \n',ssm.graph.edges(), '\n'
# Decoration of vertices:
print 'Initial Node Decoration: \n', ssm.graph['initial'], '\n'

# Hashing
print 'Instance time stame: \n', ssm.time_stamp, '\n'
print 'Initial instance digest: \n', ssm.whole_digest, '\n'

# Initial transaction (p2p platform only)
print(ssm.trans_data.get_as_dict())
ssm.export_trans_data(db_file)

# Alice offers camera on p2p platform
alice_message = 'Anyone interested in my camera? It\'s a Sony RX100 II'
alice_msg_signed = ba.b2a_hex(alice_priv.sign(alice_message))
# Add decoration to 'offered' node
ssm.update_node(node_name = 'offered',
                  sender = alice_pub_hex,
               signature = alice_msg_signed)

print 'Graph structure as string for hashing: \n', ssm.get_graph_str(), '\n'
print 'Instance digest after update: \n', ssm.whole_digest
# Look at transaction data after node update
print 'Transaction data after camera offer placed: \n', ssm.trans_data.get_as_dict()
#Export to data base
ssm.export_trans_data(db_file)

# Bob sees the post and clicks to ask about the camera
bob_message = 'Ohh, a Sony RX100 II. I would like to borrow it.'
bob_msg_signed = bob_priv.sign(bob_message)
# Add decoration to 'offered' node
ssm.update_node(node_name = 'interested',
                  sender = bob_pub_hex,
               signature = bob_msg_signed)

print 'Graph structure as string for hashing: \n', ssm.get_graph_str(), '\n'
print 'Instance digest after update: \n', ssm.whole_digest
# Look at transaction data after node update
print 'Transaction data after camera offer placed: \n', ssm.trans_data.get_as_dict()
#Export to data base
ssm.export_trans_data(db_file)

# Alice sees that Bob is interested, and applies for microinsurance with AZ

az_message = 'We can insure your Sony RX100 II for xyz under conditions abc'
az_msg_signed = az_priv.sign(az_message)
# Add decoration to 'offered' node
ssm.update_node(node_name = 'insured',
                  sender = az_pub,
               signature = az_msg_signed)

print 'Graph structure as string for hashing: \n', ssm.get_graph_str(), '\n'
print 'Instance digest after update: \n', ssm.whole_digest
# Look at transaction data after node update
print 'Transaction data after camera offer placed: \n', ssm.trans_data.get_as_dict()
#Export to data base
ssm.export_trans_data(db_file)

# Alice checks that insurance has been offered,
# and verifies that it is AZ that signed the offer

ssm.graph['insured']
check_az_key = ssm.graph['insured']['sender']
print(check_az_key.verify(ssm.graph['insured']['signature'], az_message))

# Alice ships the camera to Bob
shipped_message = 'The camera has been shipped via DHL nr 31415926535'
alice_ship_signed = alice_priv.sign(shipped_message)
# Add decoration to 'offered' node
ssm.update_node(node_name = 'transferred',
                  sender = alice_pub,
               signature = alice_ship_signed)

print 'Graph structure as string for hashing: \n', ssm.get_graph_str(), '\n'
print 'Instance digest after update: \n', ssm.whole_digest
# Look at transaction data after node update
print 'Transaction data after camera offer placed: \n', ssm.trans_data.get_as_dict()
#Export to data base
ssm.export_trans_data(db_file)

# Happy Ending
# Bob returns the camera to Alice
returned_message = 'The camera was great, shipped back via DHL nr 271828'
bob_ship_signed = bob_priv.sign(returned_message)
# Add decoration to 'offered' node
ssm.update_node(node_name = 'transferred',
                  sender = alice_pub,
               signature = alice_ship_signed)

print 'Graph structure as string for hashing: \n', ssm.get_graph_str(), '\n'
print 'Instance digest after update: \n', ssm.whole_digest
# Look at transaction data after node update
print 'Transaction data after camera offer placed: \n', ssm.trans_data.get_as_dict()
#Export to data base
ssm.export_trans_data(db_file)

# Alternative ending
# Bob doesn't return camera, AZ pays out claim (coming soon . . .)
# # Simulate posting of camera for P2P thing-lending
# # Characters:
# # Alice: has a digital camera, but rarely uses it
# # Bob: wants a camera to take pictures of family bbq next week
# # AZ: Offers microinsurance on P2P thing-lending on the blockchain
#
#
# thing = 'camera'
#
# # Issuer
# alice_priv = bc.random_key()
# alice_pub = bc.privkey_to_pubkey(alice_priv)
# print 'Alice\'s public key:', alice_pub
#
# # Interested party
# bob_priv = bc.random_key()
# bob_pub = bc.privkey_to_pubkey(bob_priv)
# print 'Bob\'s public key:', bob_pub
# # Microinsurer
# AZ_priv = bc.random_key()
# AZ_pub = bc.privkey_to_pubkey(AZ_priv)
# print 'AZ public key:', AZ_pub
#
# # P2P platform
# p2p_priv = bc.random_key()
# p2p_pub = bc.privkey_to_pubkey(p2p_priv)
# print 'P2P public key:', p2p_pub
#
# # JSON file to hold transaction data for blockchain (mock-up)
# db_file = 'p2pthing.json' # Output file for transaction data
#
# # Post offer of camera on P2P platform, back-end creates instance of SimpleSM
# ssm = csm.SimpleSM(p2p_pub) # Initialize, and track which p2p platform is calling
#
# # Initial graph
# print(ssm.graph.nodes())
# print(ssm.graph.edges())
#
# # Decoration of vertices:
# print(ssm.graph['initial'])
#
# print(ssm.whole_digest)
# print(ssm.time_stamp)
#
# # Initial transaction (p2p platform only)
# print(ssm.trans_data.get_as_dict())
# ssm.export_trans_data(db_file)
#
#
#
# # Alice offers camera on p2p platform
# # Add decoration to 'offered' node
# ssm.update_node(node_name = 'offered',
#                   sent_from = p2p_pub,
#                   sent_toby = alice_pub)
#
# print ssm.get_graph_str()
# dig2 = ssm.whole_digest
# print dig2
# t2 = ssm.time_stamp
# print t2
# print ssm.get_graph_str()
#
# # Look at transaction data after node update
# print ssm.trans_data.get_as_dict()
# ssm.export_trans_data(db_file)
# # OK, problem is with gml and adding decoration
# G = nx.DiGraph()
# G.add_node('root')
# G_gml = nx.generate_gml(G)


# #G_str = my_get_gml_str(G)
# #print(G_str)
# #g2_str = my_get_gml_str(g2)
# G['root']['test'] = 'huh'
#
# g_gml = nx.generate_gml(G)
#
# g_list = []
# try:
#     while True:
#         g_el = g_gml.next()
#         g_list.append(g_el)
# except StopIteration:
#     pass
#
#
# # Try something else
# def get_graph_dict(G):
#     g_dict = nx.to_dict_of_dicts(G)
#     return(g_dict)
#
# # Should change state digest
# ssm.state_hash_digest()
# sd_updated = ssm.state_digest()
# print(ssm.graph['offered'])
#
# ssm.update_node(node_name='offered',
#                 sent_from=issuer_pub,
#                 sent_to='everyone')
#
# def my_get_gml_str(g):
#     """
#     Returns concatented string encoding gml of graph
#     :param gml:
#     :return:
#     """
#     g_gml_orig = nx.generate_gml(g)
#     g_gml = g_gml_orig
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
#
#
# # g_str = my_get_gml_str(G)
# #g_str2 = ssm.get_gml_str()
