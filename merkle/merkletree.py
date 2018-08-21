from typing import List
import deprecation

class MerkleTree:

    def __init__(self, leave_name: str) -> None:
        self.leave_name: str = leave_name
    
    def create_tree(self, number_of_leafs: int) -> str:      
        """Main backend function which creates the string representation of the Merkle Tree (a Newick Tree)
           For furhter information visit: http://etetoolkit.org/docs/latest/tutorial/tutorial_trees.html 
        
        Arguments:
            number_of_leafs {int} -- How many leafes should the Merkle Tree have?
        
        Returns:
            str -- String representation of the Merkle Tree
        """

        leaf_pairs: List[str] = [ "({}_{},{}_{}):1".format(self.leave_name, transnumber, self.leave_name, transnumber+1)  for transnumber in range(1, number_of_leafs, 2)]             
        tree: List[str] = self.__reduce_list_by_two(leaf_pairs)
        final_tree: str = tree[0] + ";"
        return final_tree

    def __reduce_list_by_two(self, leaf_pairs: List[str]) -> List[str]:
        """[The function reduces a list with a certain number of elements by two until there is only one 
        string representation left. It uses the so called zip-clustering-idiom. For more information visit:
        https://stackoverflow.com/questions/51635881/reduce-a-list-in-a-specific-way/51636301#51636301]
        
        Arguments:
            leaf_pairs {List[str]} -- [a list which holds leafs as pairs -> one pair is one string of two leafs]
        
        Returns:
            List[str] -- [List which contains one string element --> this element is the result of the reducing process]
        """
        
        while len(leaf_pairs) > 1:
            leaf_pairs = ['({},{})'.format(x, y) for x, y in zip(*[iter(leaf_pairs)]*2)]
        return leaf_pairs

    @deprecation.deprecated(details="Function is only necessary for the deprecated reduce-function")
    def __get_blocks(self, input: int) -> List[int]:
        """[This function generates a list which contains the number of parent nodes per level in a merkle tree]      
        Arguments:
            input {int} -- [the number of leafes the merkle tree consist of]
        
        Returns:
            List[int] -- [contains the number of parent nodes per level e.g. 16 leafes lead to [4,2,1].
            8 is not included while creating the merkle tree, the leafes are already paired.]
        """
       
        initial_input: int = input
        block_list: List[int] = list()
        while input > 1:
            input = input // 2
            if(input != (initial_input // 2)):
                block_list.append(input)
        return block_list

    @deprecation.deprecated(details="This is an own implementation of the zip-clustering-idiom")
    def __reduce_list(self, leaf_pairs: List[str]) -> List[str]:
        """[The function reduces a list with a certain number of elements by two until there is only one 
        string representation left. Therefore it takes every two elements and concatenates them in a specific way (see .format).
        After one cycle the resulting list is of length len(original_list)//2. Then the cycle starts again until there is only one element in the list.]
        
        Arguments:
            leaf_pairs {List[str]} -- [a list which holds leafs as pairs -> one pair is one string of two leafs]
        
        Returns:
            List[str] -- [List which contains one string element --> this element is the result of the reducing process]
        """
       
        blocks: List[int] = self.__get_blocks(len(leaf_pairs)*2)
        for index in blocks:
            start_index: int = index*2
            for b in range(0, start_index, 2):
                element = "({},{})".format(leaf_pairs[b], leaf_pairs[b+1])
                leaf_pairs.append(element)
            del leaf_pairs[0:start_index]
        return leaf_pairs
