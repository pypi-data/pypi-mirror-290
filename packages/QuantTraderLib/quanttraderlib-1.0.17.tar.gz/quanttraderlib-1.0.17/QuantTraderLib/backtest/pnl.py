import numpy as np

def check_positions(df, min_days_between_positions=2):
    """
    Kiểm tra các vị thế mua và bán trong dữ liệu để đảm bảo chúng đáp ứng yêu cầu tối thiểu về khoảng cách giữa các vị thế.

    Tham số:
        df (pandas.DataFrame): DataFrame chứa dữ liệu với các cột 'close' và 'position'. Cột 'position' chứa giá trị 1 cho vị thế mua, -1 cho vị thế bán.
        min_days_between_positions (int, tùy chọn): Số ngày tối thiểu yêu cầu giữa các vị thế mua và bán. Mặc định là 2 ngày.

    Trả về:
        list: Danh sách các tuple chứa chỉ số của các vị thế mua và bán hợp lệ.
    """
    price_diff = df['close'].diff()
    positions = df['position']
    valid_positions = []
    invalid_positions = []
    used_sell_indices = set()
    for i in range(len(positions)):
        if positions[i] == 1:  # Nếu đây là một vị thế mua
            # Tìm vị trí bán gần nhất
            for j in range(i + 1, len(positions)):
                if positions[j] == -1 and j not in used_sell_indices:
                    # Kiểm tra khoảng cách lớn hơn 2 ngày
                    if j - i >= min_days_between_positions:
                        valid_positions.append((i, j))
                        used_sell_indices.add(j)
                    else:
                        invalid_positions.append((i, j))
                    break

    if invalid_positions:
        print("Vị thế trong dữ liệu của bạn có vài chỗ không chính xác:")
        for position in invalid_positions:
            buy_date = df.index[position[0]]
            sell_date = df.index[position[1]]
            print(f"Mua vào {buy_date}, bán vào {sell_date}")
    return valid_positions

def calculate_pnl(df):
    """
    Tính toán lợi nhuận và lỗ (PnL) dựa trên các vị thế mua và bán hợp lệ trong dữ liệu.

    Tham số:
        df (pandas.DataFrame): DataFrame chứa dữ liệu với các cột 'close' và 'position'. Cột 'position' chứa giá trị 1 cho vị thế mua, -1 cho vị thế bán.

    Trả về:
        tuple: Một tuple bao gồm hai phần tử:
            - numpy.ndarray: Mảng PnL với giá trị PnL cho các chỉ số bán.
            - list: Danh sách các tuple chứa chỉ số của các vị thế mua và bán hợp lệ.
    """
    valid_positions = check_positions(df)

    if not valid_positions:
        return None, None

    prices = df['close'].values
    pnl = np.zeros(len(prices))
    for buy_index, sell_index in valid_positions:
        buy_price = prices[buy_index]
        sell_price = prices[sell_index]
        pnl[sell_index] = sell_price - buy_price

    return pnl, valid_positions
