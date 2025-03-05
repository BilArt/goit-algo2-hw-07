import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root
        
        if key < root.key:
            if root.left is None:
                return root
            
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self._rotate_left(root.left)
            
            return root if root.left is None else self._rotate_right(root)
        
        else:
            if root.right is None:
                return root
            
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self._rotate_right(root.right)
            
            return root if root.right is None else self._rotate_left(root)
    
    def _rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right
        left_child.right = node
        return left_child

    def _rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left
        right_child.left = node
        return right_child
    
    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
            return
        
        self.root = self._splay(self.root, key)
        
        if key == self.root.key:
            return
        
        new_node = Node(key, value)
        
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        
        self.root = new_node

    def find(self, key):
        self.root = self._splay(self.root, key)
        return self.root.value if self.root and self.root.key == key else None

def fibonacci_splay(n, tree):
    if n < 2:
        return n
    
    left = tree.find(n - 1)
    if left is None:
        left = fibonacci_splay(n - 1, tree)
        tree.insert(n - 1, left)
    
    right = tree.find(n - 2)
    if right is None:
        right = fibonacci_splay(n - 2, tree)
        tree.insert(n - 2, right)
    
    return left + right

n_values = list(range(0, 1000, 50))
lru_times = []
splay_times = []

for n in n_values:
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=3) / 3
    lru_times.append(lru_time)
    
    tree = SplayTree()
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=3) / 3
    splay_times.append(splay_time)

plt.figure(figsize=(10, 6))
plt.plot(n_values, lru_times, label='LRU Cache', marker='o')
plt.plot(n_values, splay_times, label='Splay Tree', marker='x')
plt.xlabel('Число Фібоначчі (n)')
plt.ylabel('Середній час виконання (секунди)')
plt.title('Порівняння часу виконання для LRU Cache та Splay Tree')
plt.legend()
plt.grid(True)
plt.show()

print(f"{'n':<10}{'LRU Cache Time (s)':<20}{'Splay Tree Time (s)'}")
print("-" * 50)
for i in range(len(n_values)):
    print(f"{n_values[i]:<10}{lru_times[i]:<20.8f}{splay_times[i]:.8f}")
