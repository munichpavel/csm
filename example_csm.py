import bitcoin as bc
import cryptostatemachine.cryptostatemachine as csm
reload(csm)


# Simulate posting of camera for P2P thing-lending
# Characters:
# Alice: has a digital camera, but rarely uses it
# Bob: wants a camera to take pictures of family bbq next week
# AZ: Offers microinsurance on P2P thing-lending on the blockchain


thing = 'camera'

# Issuer
alice_priv = bc.random_key()
alice_pub = bc.privkey_to_pubkey(alice_priv)
print 'Alice\'s public key:', alice_pub

# Interested party
bob_priv = bc.random_key()
bob_pub = bc.privkey_to_pubkey(bob_priv)
print 'Bob\'s public key:', bob_pub
# Microinsurer
AZ_priv = bc.random_key()
AZ_pub = bc.privkey_to_pubkey(AZ_priv)
print 'AZ public key:', AZ_pub

# P2P platform
p2p_priv = bc.random_key()
p2p_pub = bc.privkey_to_pubkey(p2p_priv)
print 'P2P public key:', p2p_pub

# JSON file to hold transaction data for blockchain (mock-up)
db_file = 'p2pthing.json' # Output file for transaction data

# Post offer of camera on P2P platform, back-end creates instance of SimpleSM
ssm = csm.SimpleSM(p2p_pub) # Initialize, and track which p2p platform is calling

# Initial graph
print(ssm.graph.nodes())
print(ssm.graph.edges())

# Decoration of vertices:
print(ssm.graph['initial'])

print(ssm.whole_digest)
print(ssm.time_stamp)

# Initial transaction (p2p platform only)
print(ssm.trans_data.get_as_dict())
ssm.export_trans_data(db_file)



# Alice offers camera on p2p platform
# Add decoration to 'offered' node
ssm.update_node(node_name = 'offered',
                  sent_from = p2p_pub,
                  sent_toby = alice_pub)

print ssm.get_graph_str()
dig2 = ssm.whole_digest
print dig2
t2 = ssm.time_stamp
print t2
print ssm.get_graph_str()

# Look at transaction data after node update
print ssm.trans_data.get_as_dict()
ssm.export_trans_data(db_file)
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
