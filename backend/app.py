from flask import Flask, render_template, jsonify, request
from core.chain import Blockchain
import time
import os
import hashlib
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
template_dir = os.path.join(base_dir, 'frontend', 'templates')

app = Flask(__name__, template_folder=template_dir)
bc = Blockchain()

offchain_database = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chain')
def get_chain():
    chain_data = []
    for block in bc.chain:
        chain_data.append({
            "index": block.index,
            "timestamp": time.ctime(block.timestamp), 
            "previous_hash": block.previous_hash,     
            "merkle_root": block.merkle_root,         
            "nonce": block.nonce,                     
            "hash": block.hash,                       
            "transactions": block.transactions        
        })
    return jsonify(chain_data)

@app.route('/api/init', methods=['POST'])
def init_product():
    data = request.json
    p_id = data.get('product_id')
    details = data.get('details') 
    
    offchain_database[p_id] = details
    hash_ref = hashlib.sha256(json.dumps(details, sort_keys=True).encode('utf-8')).hexdigest()
    
    bc.add_transaction(p_id, "INIT", details, offchain_ref=hash_ref)

    mined_block = bc.mine_pending_transactions()
    
    if mined_block:
        return jsonify({"message": f"Khởi tạo thành công! Đã tạo Block #{mined_block.index}"})
    else:
        return jsonify({"message": "Khởi tạo thành công! Transaction đang chờ trong mempool."})

@app.route('/api/update', methods=['POST'])
def update_product():
    data = request.json
    p_id = data.get('product_id')
    details = data.get('details') 
    
    if not p_id or not details:
        return jsonify({"error": "Thiếu thông tin sản phẩm hoặc dữ liệu cập nhật"}), 400
    
    offchain_database[p_id] = details
    
    hash_ref = hashlib.sha256(json.dumps(details, sort_keys=True).encode('utf-8')).hexdigest()
    
    bc.add_transaction(p_id, "UPDATE", details, offchain_ref=hash_ref)
    
    mined_block = bc.mine_pending_transactions()
    
    if mined_block:
        return jsonify({
            "message": f"Cập nhật thành công! Đã tạo Block #{mined_block.index} chứa {len(mined_block.transactions)} giao dịch.",
            "block_index": mined_block.index
        })
    else:
        return jsonify({
            "message": "Cập nhật thành công! Transaction đã được thêm vào mempool và đang chờ mine khối."
        })

@app.route('/api/trace/<product_id>', methods=['GET'])
def trace(product_id):
    history = bc.trace_product(product_id)
    if not history:
        return jsonify({"error": "Không tìm thấy sản phẩm trên Blockchain"}), 404
        
    return jsonify({
        "product_id": product_id,
        "journey_length": len(history),
        "history": history
    })


@app.route('/api/get-db/<product_id>', methods=['GET'])
def get_db(product_id):
    if product_id in offchain_database:
        return jsonify({"details": offchain_database[product_id]})
    return jsonify({"error": "Sản phẩm chưa có trong Database truyền thống"}), 404

@app.route('/api/hack-db', methods=['POST'])
def hack_db():
    data = request.json
    p_id = data.get('product_id')
    tampered_details = data.get('details')
    
    if p_id in offchain_database:
        offchain_database[p_id] = tampered_details
        return jsonify({"message": "Dữ liệu trong Database đã bị thay đổi."})
    return jsonify({"error": "Không tìm thấy ID trong Database"}), 404

@app.route('/api/check-integrity/<product_id>', methods=['GET'])
def check_integrity(product_id):

    if product_id not in offchain_database:
        return jsonify({"error": "Không tìm thấy dữ liệu trong Database truyền thống"}), 404
        
    current_data = offchain_database[product_id]
    current_hash = hashlib.sha256(json.dumps(current_data, sort_keys=True).encode('utf-8')).hexdigest()
    
    original_hash = None
    for block in reversed(bc.chain): 
        for tx in block.transactions:
            if tx.get("product_id") == product_id:
                original_hash = tx.get("hash_ref") 
                break
        if original_hash: break
                
    if not original_hash:
        return jsonify({"error": "Không tìm thấy lịch sử sản phẩm trên Blockchain"}), 404
        
    # 3. Đối chiếu
    is_valid = current_hash == original_hash
    return jsonify({
        "is_valid": is_valid,
        "current_hash": current_hash,
        "original_hash": original_hash
    })

@app.route('/api/verify-tx', methods=['POST'])
def verify_transaction():
    data = request.json
    p_id = data.get('product_id')
    
    if not p_id:
        return jsonify({"error": "Thiếu mã sản phẩm"}), 400

    for i, tx in enumerate(bc.pending_transactions):
        if tx.get("product_id") == p_id:
            return jsonify({
                "is_valid": True,
                "proof_path": [],
                "message": "Giao dịch đang chờ được mine vào khối (Pending)",
                "block_index": "PENDING",
                "is_pending": True,
                "transaction_count": len(bc.pending_transactions)
            })

    for block in bc.chain:
        for i, tx in enumerate(block.transactions):
            if tx.get("product_id") == p_id:
                proof = block.merkle_tree.get_merkle_proof(i)
                is_valid = block.merkle_tree.verify_proof(tx, block.merkle_root, proof)
                
                return jsonify({
                    "is_valid": is_valid,
                    "proof_path": proof,
                    "message": "Xác thực SPV qua Merkle Tree thành công!",
                    "block_index": block.index,
                    "block_hash": block.hash[:20] + "...",
                    "transaction_count": len(block.transactions),
                    "is_single_tx": len(block.transactions) == 1,
                    "is_pending": False
                })
    
    return jsonify({"error": "Không tìm thấy giao dịch của sản phẩm này trên Blockchain"}), 404

if __name__ == '__main__':
    app.run(debug=True)