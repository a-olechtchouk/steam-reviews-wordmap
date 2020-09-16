from typing import Optional, Dict, Any, List
# ~~~~~~~~~~~~~~~~~ NOTE: START OF WIKI CLASS AND FUNCTIONS THAT ARE NOT MY OWN ~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~ NOTE: FROM THE WIKI PAGE: https://en.wikipedia.org/wiki/Trie#A_Python_version ~~~~~~~~~~~~~~~~~
class Node:
    def __init__(self) -> None:
        # Note that using a dictionary for children (as in this implementation)
        # would not by default lexicographically sort the children, which is
        # required by the lexicographic sorting in the Sorting section.
        # For lexicographic sorting, we can instead use an array of Nodes.
        # self.children: Dict[str, Node] = {}          # mapping from character to Node
        self.children: Dict[str, Optional[Node]] = {}  # mapping from character to a list of nodes
        self.value: Optional[Any] = None

def find(node: Node, key: str) -> Optional[Any]:
    # Find value by key in node.
    for char in key:
        if char in node.children:
            node = node.children[char]
        else:
            return None
    return node.value

def insert(node: Node, key: str, value: Any) -> None:
# Insert key/value pair into node.
    for char in key:
        if char not in node.children:
            node.children[char] = Node()
        node = node.children[char]
    node.value = value

def delete(root: Node, key: str) -> bool:
    # Eagerly delete the key from the trie rooted at `root`.
    # Return whether the trie rooted at `root` is now empty.
    
    def _delete(node: Node, key: str, d: int) -> bool:
        # Clear the node corresponding to key[d], and delete the child key[d+1]
        # if that subtrie is completely empty, and return whether `node` has been
        # cleared.
        if d == len(key):
            node.value = None
        else:
            c = key[d]
            if c in node.children and _delete(node.children[c], key, d+1):
                del node.children[c]
        # Return whether the subtrie rooted at `node` is now completely empty
        return node.value is None and len(node.children) == 0

    return _delete(root, key, 0)

def keys_with_prefix(root: Node, prefix: str) -> List[str]:
    results: List[str] = []
    x = _get_node(root, prefix)
    _collect(x, list(prefix), results)
    return results

def _collect(x: Optional[Node], prefix: List[str], results: List[str]) -> None:
    # Append keys under node `x` matching the given prefix to `results`.
    # prefix: list of characters
    if x is None:
        return
    if x.value is not None:
        prefix_str = ''.join(prefix)
        results.append(prefix_str)
    for c in x.children:
        prefix.append(c)
        _collect(x.children[c], prefix, results)
        del prefix[-1]  # delete last character
    
def _get_node(node: Node, key: str) -> Optional[Node]:
    # Find node by key. This is the same as the `find` function defined above,
    # but returning the found node itself rather than the found node's value.
    for char in key:
        if char in node.children:
            node = node.children[char]
        else:
            return None
    return node
# ~~~~~~~~~~~~~~~~~ NOTE: END OF WIKI CLASS AND FUNCTIONS THAT ARE NOT MY OWN ~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~ NOTE: FROM THE WIKI PAGE: https://en.wikipedia.org/wiki/Trie#A_Python_version ~~~~~~~~~~~~~~~~~



# NOTE: ~~~~~~~~~~~~~~~~~ START OF MY OWN FUNCTIONS THAT I WROTE ~~~~~~~~~~~~~~~~~

# build the Trie using a sorted list of Steam application tuples (name, appid)
def build_trie_from_games(games: list):
    root_trie = Node()
    for game in games:
        game = tuple(game)
        insert(root_trie, game[0], game[1])
    return root_trie

def search_trie(root: Node, prefix: str):
    search_results = keys_with_prefix(root, prefix)
    return search_results