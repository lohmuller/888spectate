from collections import Counter


def find_internal_nodes_num(input_list):
    """
    Counts the internal nodes in a generic tree defined by the given input list.

    In the context of this problem, a tree is represented by consecutive integers in the input list.
    Each element in the input list represents a node, and its value is the parent node's index.
    The root node is denoted by -1. Internal nodes are nodes with at least one child.

    The logic to count internal nodes is to count unique values in the input list, excluding the root node (-1).
    This approach has a time complexity of O(n), where n is the number of elements in the input list.
    The Counter function operates in O(n) time, and calculating the length of the counts dictionary is O(1).

    Args:
        input_list (list): List representing the tree nodes and their parent indices.

    Returns:
        int: Number of internal nodes in the tree.
    """

    # Counting unique values using Counter
    counts = Counter(input_list)

    # Subtract 1 to exclude the value "-1" (root)
    return len(counts) - 1


# Example usage
my_tree = [4, 4, 1, 5, -1, 4, 5]
print(find_internal_nodes_num(my_tree))  # Output: 3
