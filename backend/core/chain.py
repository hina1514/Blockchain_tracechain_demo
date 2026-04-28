import time
from typing import List, Dict
from core.block import Block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = [] 
        self.create_genesis()

    def create_genesis(self):
        genesis_tx = {
            "product_id": "SYSTEM",
            "action": "GENESIS",
            "details": {"message": "Khởi tạo mạng lưới TraceChain VN"},
            "timestamp": time.time(),
            "hash_ref": ""
        }
        genesis = Block(0, "0", [genesis_tx])
        self.chain.append(genesis)

    def add_transaction(self, product_id: str, action: str, details: dict, offchain_ref: str = ""):
        """Thêm giao dịch vào mempool"""
        transaction = {
            "product_id": product_id,
            "action": action,
            "details": details,
            "timestamp": int(time.time()),      
            "hash_ref": offchain_ref
        }
        self.pending_transactions.append(transaction)
        return transaction

    def mine_pending_transactions(self, miner_address="SYSTEM"):
        """Đào khối chỉ khi có ít nhất 2 transaction, hoặc ép buộc"""
        if len(self.pending_transactions) < 2:
            return None  
        
        prev_hash = self.chain[-1].hash
        new_block = Block(len(self.chain), prev_hash, self.pending_transactions.copy())
        
        target = "0" * 3
        while new_block.hash[:3] != target:
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()
            
        self.chain.append(new_block)
        self.pending_transactions.clear()
        
        print(f"✅ Đã mine thành công Block #{new_block.index} với {len(new_block.transactions)} transactions")
        return new_block

    def trace_product(self, product_id: str) -> List[Dict]:
        """Truy xuất lịch sử sản phẩm - tìm cả trong pending_transactions và chain"""
        history = []

        for tx in self.pending_transactions:
            if tx.get("product_id") == product_id:
                history.append(tx)

        for block in self.chain:
            for tx in block.transactions:
                if tx.get("product_id") == product_id:
                    history.append(tx)

        history.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
        
        return history

    def get_transaction_by_product(self, product_id: str):
        """Lấy giao dịch mới nhất của sản phẩm (dùng cho verify-tx)"""
        for block in reversed(self.chain):   
            for tx in block.transactions:
                if tx.get("product_id") == product_id:
                    return tx, block
        return None, None