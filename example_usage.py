from merkle.merkletreeplot import MerkleTreePlot

# create a merkle tree with 32 leafes 
tree = MerkleTreePlot(32)

# highlight nodes which are necessary to confirm that particular leaf (24) is in merkle tree
#tree.mark_verification_nodes(24, "yellow")

# highlight nodes which will change when one leaf (here leaf 24) is changed
tree.change_leaf(24)

# rotate the merkle tree
tree.rotation = 90

# plot the tree
tree.plot_merkletree()

# Note: You can either highlight the verification nodes or change a leaf and highlight all nodes in the branch of the leaf