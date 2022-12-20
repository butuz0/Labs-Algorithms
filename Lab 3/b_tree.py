from b_tree_node import BTreeNode


class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)
        self.t = t
        self.print_text = []
        self.max_length = 2 * t - 1
        self.min_length = t - 1
        self.compares = 0

    def insert(self, key):
        root = self.root
        if len(root.keys) == self.max_length:
            temp = BTreeNode()
            self.root = temp
            temp.children.insert(0, root)
            self.split_child(temp, 0)
            self.insert_non_full(temp, key)
        else:
            self.insert_non_full(root, key)

    def insert_non_full(self, node, key):
        i = len(node.keys) - 1
        while i >= 0 and key[0] < node.keys[i][0]:
            i -= 1
        i += 1
        if node.is_leaf:
            node.keys.insert(i, key)
        else:
            if len(node.children[i].keys) == self.max_length:
                self.split_child(node, i)
                if key[0] > node.keys[i][0]:
                    i += 1
            self.insert_non_full(node.children[i], key)

    def split_child(self, node, i):
        t = self.t
        y = node.children[i]
        z = BTreeNode(y.is_leaf)
        node.children.insert(i + 1, z)
        node.keys.insert(i, y.keys[t-1])
        z.keys = y.keys[t:]
        y.keys = y.keys[:t-1]
        if not y.is_leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]

    def print_tree(self, node, level=0, first_run=True):
        if first_run:
            self.print_text = []
        if len(self.print_text) <= level:
            self.print_text.append("")
        for key in node.keys:
            self.print_text[level] += f"{key[0]}|"
        self.print_text[level] = self.print_text[level][:-1]
        self.print_text[level] += "  "
        if len(node.children) > 0:
            for child in node.children:
                self.print_tree(child, level+1, False)
            self.print_text[level+1] += "\t"
            self.print_text[level] += "\t\t"
        return self.print_text

    def uniform_bin_search(self, key, node: BTreeNode, parent=None):
        i = len(node.keys) // 2
        delta = len(node.keys) // 2
        while delta != 0:
            self.compares += 1
            delta = delta // 2
            if i >= len(node.keys) or node.keys[i][0] > key:
                i -= (delta + 1)
            elif node.keys[i][0] < key:
                i += delta + 1
            else:
                return i, node, parent
        if i == len(node.keys):
            i -= 1
        if i < 0:
            i = 0

        if node.keys[i][0] == key:
            return i, node, parent
        if node.is_leaf:
            return None, None, None
        else:
            if node.keys[i][0] > key:
                return self.uniform_bin_search(key, node.children[i], parent=node)
            else:
                return self.uniform_bin_search(key, node.children[i+1], parent=node)

    def replace(self, key, value):
        index, node, parent = self.uniform_bin_search(key, self.root)
        if node is not None:
            node.keys.pop(index)
            node.keys.insert(index, (key, value))

    def console_print(self, x, level=0):
        print("Level ", level, " ", len(x.keys), end=":")
        for i in x.keys:
            print(i, end=" ")
        print()
        level += 1
        if len(x.children) > 0:
            for i in x.children:
                self.console_print(i, level)

    def delete_key(self, key):
        i, node, parent = self.uniform_bin_search(key, self.root)
        if not node:
            return False

        if node.is_leaf:
            # if root is the only node in tree - delete key
            # or node is a leaf with enough elements
            if node == self.root or len(node.keys) > self.min_length:
                node.keys.pop(i)        # simple deletion from the leaf
            else:
                self.pop_element(key)
                self.empty_delete(parent, node)     # deal with siblings if node has minimum of keys
        else:
            if len(node.keys) > self.min_length:
                if len(node.children[i].keys) > self.min_length:
                    self.delete_predecessor(node, i)
                elif len(node.children[i+1].keys) > self.min_length:
                    self.delete_successor(node, i)
                else:
                    self.merge(node, i, i+1)        # merge left and right children if both have minimum of keys
            else:
                self.pop_element(key)
                self.empty_delete(parent, node)     # deal with siblings if node has minimum of keys
        return True

    def empty_delete(self, parent, node):
        index = parent.children.index(node)

        if index > 0 and len(parent.children[index - 1].keys) > self.min_length:
            self.swap_sibling(parent, index, index-1)       # swapping with left sibling

        elif index < len(parent.children) - 1 and len(parent.children[index + 1].keys) > self.min_length:
            self.swap_sibling(parent, index, index+1)       # swapping with right sibling
        else:
            if index > 0:
                self.merge(parent, index, index-1)      # merging with left sibling
            else:
                self.merge(parent, index, index+1)      # merging with right sibling

        if node == self.root:
            return

        # make sure the structure of B-Tree is not violated
        while len(parent.keys) < self.min_length and parent != self.root:
            i, node, parent = self.uniform_bin_search(parent.keys[0][0], self.root)
            self.empty_delete(parent, node)

    def pop_element(self, key):
        index, node, parent = self.uniform_bin_search(key, self.root)
        node.keys.pop(index)

    @staticmethod
    def swap_sibling(node, i, j):
        parent = node
        node = parent.children[i]
        sibling = parent.children[j]
        if i > j:
            key = sibling.keys.pop()
            node.keys.insert(0, parent.keys.pop(i - 1))
            parent.keys.insert(i - 1, key)
            if not node.is_leaf:
                parent.children[j].children[-2].keys += parent.children[j].children[-1].keys
                parent.children[j].children.pop()
                node.children[0].keys.insert(0, node.keys.pop(0))
                node.keys.insert(0, node.children[0].keys.pop())
        else:
            key = sibling.keys.pop(0)
            node.keys.append(parent.keys.pop(i))
            parent.keys.insert(i, key)
            if not node.is_leaf:
                parent.children[j].children[0].keys += parent.children[j].children[1].keys
                parent.children[j].children.pop(1)
                node.children[-1].keys.append(node.keys.pop())
                node.keys.append(node.children[-1].keys.pop(0))

    @staticmethod
    def delete_predecessor(node, i):
        parent = node
        node = parent.children[i]
        parent.keys.pop(i)
        parent.keys.insert(i, node.keys.pop())

    @staticmethod
    def delete_successor(node, i):
        parent = node
        node = parent.children[i+1]
        parent.keys.pop(i)
        parent.keys.insert(i, node.keys.pop(0))

    def merge(self, node, i, j):
        parent = node
        child = parent.children[i]
        sibling = parent.children[j]

        if i > j:
            sibling.keys += [parent.keys.pop(j)] + child.keys
        else:
            child.keys += [parent.keys.pop(i)] + sibling.keys

        if not child.is_leaf:
            parent.children[i].children += parent.children[j].children

        if i > j:
            parent.children.pop(i)
        else:
            parent.children.pop(j)

        if parent == self.root and len(parent.keys) == 0:
            self.root = sibling if i > j else child
            self.root.is_leaf = True
