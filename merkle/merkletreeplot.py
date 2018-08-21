from merkle.merkletree import MerkleTree
from ete3 import Tree, NodeStyle, TreeStyle, TreeNode

class MerkleTreePlot():

    def __init__(self, number_of_leafs: int, leave_name="leaf") -> None:
        self.merkle_tree: MerkleTree = MerkleTree(leave_name)
        self.merkle_tree_plot: Tree = Tree( self.merkle_tree.create_tree(number_of_leafs) )
        self.node_style_color: str = "green"
        self.rotation: int = 0
        self.is_change: bool = False

    def __get_tree_style(self) -> TreeStyle:
        """Private function for creating a defined TreeStyle for the tree.
        
        Returns:
            TreeStyle -- Fixed TreeStyle - only rotation can be altered.
        """

        tree_style: TreeStyle = TreeStyle()
        tree_style.show_leaf_name = True
        tree_style.rotation = self.rotation
        tree_style.min_leaf_separation = 25
        tree_style.show_scale = False
        return tree_style

    def __get_general_nodestyle(self, color: str = None) -> NodeStyle:
        """Private function which is used to set NodeStyle for all nodes which is applied to.
        
        Keyword Arguments:
            color {str} -- see etetoolkit documentation for all available colors. (default: {None})
        
        Returns:
            NodeStyle
        """

        node_style: NodeStyle = NodeStyle()
        node_style["shape"] = "sphere"
        node_style["size"] = 10
        if(color is None):
            node_style["fgcolor"] = self.node_style_color
        else:
            node_style["fgcolor"] = color
        node_style["hz_line_type"] = 1
        node_style["hz_line_color"] = "#cccccc"
        return node_style

    def __set_node_style(self):
        """Private function which set a default NodeStyle.
        """

        for node in self.merkle_tree_plot.traverse():
            local_node_style: NodeStyle = self.__get_general_nodestyle()
            node.set_style(local_node_style)

    def change_leaf(self, leaf_number: int, color = "darkred"):
        """Function which alters a leaf and all nodes in the particular branch of the selected leaf.
           Altered nodes are highlighted in the specified color.
        
        Arguments:
            leaf_number {int} -- Number of leave to alter
        
        Keyword Arguments:
            color {str} -- Color which will be used for highlighting changed nodes (default: {"darkred"})
        """

        self.__set_node_style()
        node_to_find: TreeNode = self.__find_node(leaf_number)
        while node_to_find:
            change_node_style: NodeStyle = self.__get_general_nodestyle(color)
            node_to_find.set_style(change_node_style)    
            node_to_find = node_to_find.up

    def mark_verification_nodes(self, leaf_number: int, color = "purple"):
        """Function which highlights all nodes which are necessary to find a specific leaf in the tree.
        
        Arguments:
            leaf_number {int} -- leaf number which should be verified.
        
        Keyword Arguments:
            color {str} -- Color which will be used for highlighting verification nodes (default: {"purple"})
        """

        self.__set_node_style()
        node_to_find: TreeNode = self.__find_node(leaf_number)
        while node_to_find:
            verification_node_style: NodeStyle = self.__get_general_nodestyle(color)
            if(not node_to_find.is_root()):
                sister_node: TreeNode = node_to_find.get_sisters()[0]
                sister_node.name = "verification_node_for_leaf_{}".format(leaf_number)
                sister_node.set_style(verification_node_style)
                node_to_find = node_to_find.up
            else:
                node_to_find.set_style(verification_node_style)
                break


    def __find_node(self, leaf_number: int) -> TreeNode:
        """Private Function which identifies the leaf which should be altered (change_leaf()) or confirmed (mark_verification_nodes())
        
        Arguments:
            leaf_number {int} -- leaf-number for finding the correct leaf
        
        Returns:
            TreeNode -- TreeNode of found leaf
        """

        leaf_to_search: str = '{}_{}'.format(self.merkle_tree.leave_name, leaf_number)
        try:
            node_to_find: TreeNode = self.merkle_tree_plot.search_nodes(name=leaf_to_search)[0]
            self.is_change = True
            return node_to_find
        except IndexError as ie:
            print(ie)
            print("No leaf {} available due to not processable leaf-number for merkle tree.".format(leaf_number))
            print("Number of leafes to display should be: 2^(n+1)")

    def plot_merkletree(self, root_node_color="blue"):
        """Main function to plot the MerkleTree.
        
        Keyword Arguments:
            root_node_color {str} -- Color of root node is only set in simple Merkle Tree without modification (default: {"blue"})
        """

        if(not self.is_change):
            self.__set_node_style()
            self.merkle_tree_plot.img_style["fgcolor"] = root_node_color
        self.merkle_tree_plot.show(tree_style=self.__get_tree_style())
