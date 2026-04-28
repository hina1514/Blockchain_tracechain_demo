# DEMO hệ thống theo dõi chuỗi cung ứng sử dụng công nghệ **Blockchain**

## Giới thiệu
Mo phong cách Blockchain có thể chống giả mạo dữ liệu, đảm bảo tính toàn vẹn và minh bạch trong quá trình sản xuất - vận chuyển - tiêu thụ trong thương mại điện tử


## Công nghệ sử dụng

- **Backend**: Python + Flask
- **Blockchain**: Self-implemented Blockchain (Proof of Work đơn giản)
- **Cấu trúc dữ liệu**: Hybrid Storage (Off-chain Database + On-chain)
- **Merkle Tree**: Xác thực giao dịch (SPV)
- **Frontend**: HTML + Bootstrap 5 + JavaScript
- **Database**: In-memory (Dictionary)

## Tính năng chính

### 1. Khởi tạo Lô hàng 
- Đăng ký thông tin lô hàng mới (Mã lô, nguồn gốc, chứng nhận)
- Lưu dữ liệu vào Off-chain Database và tạo transaction trên Blockchain

### 2. Cập nhật Logistics
- Cập nhật thông tin theo dõi (nhiệt độ, độ ẩm, trạng thái vận chuyển)
- Mỗi lần cập nhật tạo transaction mới trên chuỗi khối

### 3. Truy vết (Traceability)
- Tra cứu toàn bộ lịch sử của một lô hàng
- Hiển thị hành trình theo dạng Timeline

### 4. Block Explorer
- Xem toàn bộ chuỗi khối
- Hiển thị chi tiết từng block, Merkle Root, transactions

### 5. Demo giả mạo dữ liệu
- Mô phỏng hacker sửa dữ liệu trong cơ sở dữ liệu truyền thống
- Kiểm tra tính toàn vẹn dữ liệu bằng cách so sánh hash giữa DB và Blockchain
- Phát hiện ngay lập tức khi dữ liệu bị giả mạo

## Hướng dẫn cài đặt và chạy

### 1. Clone dự án
```bash
git clone https://github.com/hina1514/Blockchain_tracechain_demo.git
cd Blockchain_tracechain_demo
```

### 2. Tạo và kích hoạt môi trường ảo
```bash
python -m venv venv
venv\Scripts\activate     # Windows
# source venv/bin/activate   # MacOS/Linux
```

### 3. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 4. Chạy ứng dụng
```bash
cd backend
python app.py
```

Truy cập: **http://127.0.0.1:5000**

---

## Hướng dẫn sử dụng

1. **Khởi tạo**: Tạo lô hàng mới
2. **Cập nhật**: Thêm thông tin logistics (nhiệt độ, độ ẩm, trạng thái)
3. **Truy vết**: Nhập mã lô hàng để xem toàn bộ lịch sử
4. **Block Explorer**: Xem chi tiết các khối đã được tạo
5. **Demo Tấn công DB**:
   - Nhập ID lô hàng → Tải dữ liệu
   - Sửa dữ liệu trong textarea
   - Thực thi hack
   - Nhấn "Quét Toàn vẹn" để kiểm tra
---

## Nhóm thực hiện

- **Nhóm 10** - Báo cáo An toàn Bảo mật Mạng