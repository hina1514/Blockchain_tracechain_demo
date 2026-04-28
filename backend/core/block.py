import hashlib
import time
import json
from typing import List, Dict
from .merkle import MerkleTree   

class Block:
    def __init__(self, index: int, previous_hash: str, transactions: List[Dict]):
        self.index = index
        self.timestamp = int(time.time())          
        self.previous_hash = previous_hash
        self.transactions = transactions          
        self.nonce = 0

        self.merkle_tree = MerkleTree(transactions)   
        self.merkle_root = self.merkle_tree.get_merkle_root()

        # Tính hash của block
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Tính hash của block"""
        block_header = f"{self.index}{self.timestamp}{self.previous_hash}{self.merkle_root}{self.nonce}"
        return hashlib.sha256(block_header.encode('utf-8')).hexdigest()

    def get_transaction_count(self) -> int:
        return len(self.transactions)