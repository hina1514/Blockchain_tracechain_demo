import hashlib
import json
from typing import List, Tuple, Dict, Any

class MerkleTree:
    def __init__(self, transactions: List[Dict] = None):
        self.transactions = transactions or []
        self.leaves: List[str] = []
        self.tree: List[List[str]] = []
        self.root: str = ""
        
        if self.transactions:
            self.build()

    def hash_data(self, data: Any) -> str:
        if isinstance(data, dict):
            data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
        else:
            data_str = str(data)
        return hashlib.sha256(data_str.encode('utf-8')).hexdigest()

    def build(self):
        if not self.transactions:
            self.root = hashlib.sha256(b"").hexdigest()
            return

        self.leaves = [self.hash_data(tx) for tx in self.transactions]
        current_level = self.leaves[:]
        self.tree = [current_level[:]]

        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                parent = hashlib.sha256((left + right).encode('utf-8')).hexdigest()
                next_level.append(parent)
            current_level = next_level
            self.tree.append(current_level[:])

        self.root = self.tree[-1][0]

    def get_merkle_root(self) -> str:
        return self.root

    def get_merkle_proof(self, leaf_index: int) -> List[Tuple[str, str]]:
        if not self.tree or leaf_index < 0 or leaf_index >= len(self.leaves):
            return []

        proof = []
        index = leaf_index
        level = 0

        while level < len(self.tree) - 1:
            current_level = self.tree[level]
            is_right = (index % 2 == 1)

            sibling_idx = index - 1 if is_right else index + 1
            direction = "left" if is_right else "right"

            if sibling_idx >= len(current_level):
                sibling_idx = index
                direction = "duplicate"

            proof.append((current_level[sibling_idx], direction))
            index //= 2
            level += 1

        return proof

    def verify_proof(self, leaf_data: Dict, merkle_root: str, proof: List[Tuple[str, str]]) -> bool:
        if not proof:
            return len(self.transactions) == 1 and self.hash_data(leaf_data) == merkle_root

        current = self.hash_data(leaf_data)

        for sibling, direction in proof:
            if direction in ["left", "duplicate"]:
                current = hashlib.sha256((sibling + current).encode('utf-8')).hexdigest()
            else:
                current = hashlib.sha256((current + sibling).encode('utf-8')).hexdigest()

        return current == merkle_root