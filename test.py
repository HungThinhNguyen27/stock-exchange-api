import pandas as pd


def recommend_lowest_price(stock_data):
    # Kiểm tra xem dữ liệu cổ phiếu có tồn tại không
    if stock_data.empty:
        return None

    # Sắp xếp dữ liệu theo giá tăng dần và lấy giá thấp nhất
    lowest_price_stock = stock_data.sort_values(by='price').iloc[0]

    return lowest_price_stock

# Ví dụ về cách sử dụng
# Giả sử stock_data là DataFrame chứa thông tin về các cổ phiếu
# stock_data có thể được tải từ nguồn dữ liệu như API chứng khoán
# hoặc các nguồn dữ liệu khác


# Tạo một DataFrame giả định
data = {'symbol': ['AAPL', 'GOOGL', 'MSFT', 'AMZN'],
        'price': [1500.0, 2500.0, 3000.0, 1800.0]}

stock_data = pd.DataFrame(data)

# Đề xuất cổ phiếu có giá thấp nhất
recommended_stock = recommend_lowest_price(stock_data)

if recommended_stock is not None:
    print(
        f"Đề xuất mua cổ phiếu {recommended_stock['symbol']} với giá {recommended_stock['price']}")
else:
    print("Không có dữ liệu cổ phiếu.")
