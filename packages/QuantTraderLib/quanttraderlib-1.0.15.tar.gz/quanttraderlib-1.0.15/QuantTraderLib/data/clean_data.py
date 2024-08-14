from datetime import datetime, timedelta
import lunardate
import pandas as pd
import numpy as np

######################################## helper functions #######################################
def _find_date_column(df):
    possible_date_columns = ['date', 'Date', 'time', 'Time']
    for col in possible_date_columns:
        if col in df.columns:
            return col
    raise ValueError("No date column found in DataFrame.")

def _find_column(df, column_names):
    for col in column_names:
        if col in df.columns:
            return col
    raise ValueError("No column found in DataFrame with names: " + ", ".join(column_names))

def _generate_time_slots(start, end, interval_minutes):
    time_slots = []
    current_time = start
    while current_time < end:
        time_slots.append(current_time)
        current_time += timedelta(minutes=interval_minutes)
    return time_slots

def _create_valid_minutes():
    valid_times = []
    morning_session = _generate_time_slots(datetime.strptime("09:00", "%H:%M"), datetime.strptime("11:30", "%H:%M"), 1)
    afternoon_session_1 = _generate_time_slots(datetime.strptime("13:00", "%H:%M"), datetime.strptime("14:30", "%H:%M"), 1)
    valid_times.extend(morning_session)
    valid_times.extend(afternoon_session_1)
    valid_times.append(datetime.strptime("14:45", "%H:%M"))
    return valid_times

def drop_duplicated_values(df):

    data = df.set_index('Date') #, inplace =True)
    data.columns = ['Open','High','Low','Close','Volume']

    data['Date'] = [str(i)[:10] for i in data.index]
    data['time'] = [str(i)[11:] for i in data.index]
    # Handling duplicate
    data = data[~data.index.duplicated(keep='first')]

    return data

############################################ CLEAN DAILY DATA ##############################################################
def get_vietnam_trading_days(start_date, end_date):
    """
    Tạo danh sách các ngày giao dịch tại Việt Nam trong khoảng thời gian cụ thể, loại bỏ ngày cuối tuần và ngày lễ.

    Tham số:
        start_date (str hoặc datetime): Ngày bắt đầu cho danh sách ngày giao dịch. Định dạng: 'YYYY-MM-DD'.
        end_date (str hoặc datetime): Ngày kết thúc cho danh sách ngày giao dịch. Định dạng: 'YYYY-MM-DD'.

    Trả về:
        list: Danh sách các ngày giao dịch trong khoảng thời gian đã chỉ định.
    """
    # Tạo danh sách các ngày trong khoảng thời gian
    date_range = pd.date_range(start_date, end_date)

    # Loại bỏ các ngày cuối tuần (Thứ 7, Chủ nhật)
    trading_days = date_range[date_range.weekday < 5]

    # Lấy các năm trong khoảng thời gian
    years = list(set(date_range.year))

    all_holidays = []

    for year in years:
        # Danh sách các ngày lễ (dạng datetime)
        holidays = [
            datetime(year, 1, 1),  # Tết Dương lịch
            datetime(year, 4, 30),  # Ngày Giải phóng miền Nam
            datetime(year, 5, 1),  # Ngày Quốc tế Lao động
            datetime(year, 9, 2)  # Ngày Quốc khánh
        ]

        # Tính ngày Tết Nguyên Đán
        lunar_new_year = lunardate.LunarDate(year, 1, 1).toSolarDate()
        tet_holidays = [lunar_new_year + timedelta(days=i) for i in range(7)]  # Tết Nguyên Đán kéo dài 7 ngày
        holidays.extend(tet_holidays)

        # Tính ngày Giỗ tổ Hùng Vương (10 tháng 3 âm lịch)
        hung_vuong_anniversary = lunardate.LunarDate(year, 3, 10).toSolarDate()
        holidays.append(hung_vuong_anniversary)

        # Thêm các ngày lễ vào danh sách tổng
        all_holidays.extend(holidays)

    # Loại bỏ các ngày lễ khỏi danh sách ngày giao dịch
    trading_days = [day for day in trading_days if day not in all_holidays]

    return trading_days

def check_missing_trading_dates(df):
    """
    Kiểm tra các ngày giao dịch bị thiếu trong DataFrame so với danh sách các ngày giao dịch tại Việt Nam.

    Tham số:
        df (pandas.DataFrame): DataFrame chứa dữ liệu giao dịch với ít nhất một cột ngày.

    Trả về:
        pandas.DataFrame: DataFrame chứa các ngày giao dịch bị thiếu.
    """
    date_col = _find_date_column(df)

    # Đảm bảo cột date có kiểu dữ liệu datetime
    df[date_col] = pd.to_datetime(df[date_col])

    # Xác định ngày bắt đầu và ngày kết thúc từ cột date của dataframe
    start_date = df[date_col].min()
    end_date = df[date_col].max()

    # Lấy danh sách các ngày giao dịch
    trading_days = get_vietnam_trading_days(start_date, end_date)

    # Chuyển đổi danh sách các ngày giao dịch thành DataFrame để dễ so sánh
    trading_days_df = pd.DataFrame(trading_days, columns=[date_col])

    # Kiểm tra các ngày thiếu trong dữ liệu
    missing_dates = trading_days_df[~trading_days_df[date_col].isin(df[date_col])]

    return missing_dates

def fill_missing_days(df):
    """
    Điền các ngày giao dịch bị thiếu trong DataFrame bằng cách thêm các ngày thiếu và sử dụng phương pháp forward-fill.

    Tham số:
        df (pandas.DataFrame): DataFrame chứa dữ liệu giao dịch với ít nhất một cột ngày.

    Trả về:
        pandas.DataFrame: DataFrame với các ngày giao dịch bị thiếu đã được điền và dữ liệu đã được fill.
    """
    date_col = _find_date_column(df)

    # Đảm bảo cột date có kiểu dữ liệu datetime
    df[date_col] = pd.to_datetime(df[date_col])

    # Xác định ngày bắt đầu và ngày kết thúc từ cột date của dataframe
    start_date = df[date_col].min()
    end_date = df[date_col].max()

    # Lấy danh sách các ngày giao dịch
    trading_days = get_vietnam_trading_days(start_date, end_date)

    # Chuyển đổi danh sách các ngày giao dịch thành DataFrame để dễ so sánh
    trading_days_df = pd.DataFrame(trading_days, columns=[date_col])
    trading_days_df[date_col] = pd.to_datetime(trading_days_df[date_col])

    # Tìm các ngày giao dịch bị thiếu trong dữ liệu
    missing_dates = trading_days_df[~trading_days_df[date_col].isin(df[date_col])]

    if not missing_dates.empty:
        # Tạo một DataFrame cho các ngày thiếu và gán giá trị NaN cho các cột còn lại
        missing_dates = missing_dates.set_index(date_col)
        missing_df = pd.DataFrame(index=missing_dates.index, columns=df.columns.drop(date_col))
        missing_df.reset_index(inplace=True)

        # Kết hợp DataFrame gốc với DataFrame các ngày thiếu
        df = pd.concat([df, missing_df]).sort_values(by=date_col).reset_index(drop=True)

        # Áp dụng phương pháp ffill để điền các giá trị OHLCV
        df.fillna(method='ffill', inplace=True)

    return df

############################################ CLEAN MINUTE DATA ##############################################################
def check_missing_minutes(data, date_col_candidates=['date', 'Date'], time_col_candidates=['time', 'Time']):
    """
    Kiểm tra các phút bị thiếu trong dữ liệu theo từng phút.

    Tham số:
        data (pandas.DataFrame): DataFrame chứa dữ liệu theo từng phút với ít nhất một cột ngày và một cột giờ.
        date_col_candidates (list, tùy chọn): Danh sách các tên cột có thể chứa ngày. Mặc định là ['date', 'Date'].
        time_col_candidates (list, tùy chọn): Danh sách các tên cột có thể chứa giờ. Mặc định là ['time', 'Time'].

    Trả về:
        dict: Từ điển với ngày là khóa và danh sách các phút bị thiếu trong ngày đó là giá trị.
    """
    try:
        # Tìm cột ngày và giờ riêng biệt
        date_column = _find_column(data, date_col_candidates)
        time_column = _find_column(data, time_col_candidates)
        # Chuyển đổi cột ngày và giờ
        data[date_column] = pd.to_datetime(data[date_column])
        data[time_column] = pd.to_datetime(data[time_column], format='%H:%M:%S').dt.time

        # Tạo danh sách datetime tạm thời
        datetimes = data.apply(lambda row: datetime.combine(row[date_column].date(), row[time_column]), axis=1)
    except ValueError:
        # Nếu không có cột giờ, kiểm tra xem có cột ngày giờ không
        datetime_column = _find_column(data, date_col_candidates)
        datetimes = pd.to_datetime(data[datetime_column])

    valid_times = _create_valid_minutes()

    missing_times_per_day = {}

    for day in datetimes.dt.date.unique():
        day_data = datetimes[datetimes.dt.date == day]
        day_times = day_data.dt.strftime('%H:%M').tolist()
        valid_day_times = [datetime.combine(day, time.time()).strftime('%H:%M') for time in valid_times]

        missing_times = set(valid_day_times) - set(day_times)

        # Delete future times
        now = datetime.now()
        if day >= now.date():
            # Ensure times are only relevant if they are today or earlier
            missing_times = {time for time in missing_times if datetime.combine(day, datetime.strptime(time, '%H:%M').time()) <= now}

        if missing_times:  # Chỉ thêm nếu có thời gian bị thiếu
            missing_times_per_day[day] = sorted(list(missing_times))

    return missing_times_per_day

def fill_missing_minutes(df, missing_times_per_day):
    """
    Điền các phút bị thiếu trong dữ liệu theo từng phút.

    Tham số:
        df (pandas.DataFrame): DataFrame chứa dữ liệu theo từng phút với ít nhất một cột ngày và một cột giờ.
        missing_times_per_day (dict): Từ điển chứa các phút bị thiếu cho từng ngày.

    Trả về:
        pandas.DataFrame: DataFrame với các phút bị thiếu đã được điền và dữ liệu đã được fill.
    """
    # Đảm bảo các cột được đặt tên đúng
    df.columns = [col.capitalize() for col in df.columns]
    
    # Kiểm tra và thêm các cột thiếu với giá trị NaN
    required_columns = ['Open', 'High', 'Low', 'Close']
    for col in required_columns:
        if col not in df.columns:
            df[col] = np.nan
    
    # Đặt 'Date' làm chỉ mục và reset chỉ mục cho tiện xử lý
    data = df.set_index(_find_date_column(df))
    
    # Tách ngày và giờ từ chỉ mục
    data['Date'] = [str(i)[:10] for i in data.index]  # Lấy phần ngày từ chỉ mục datetime
    data['Time'] = [str(i)[11:] for i in data.index]  # Lấy phần giờ từ chỉ mục datetime

    # Xử lý các bản sao
    data = data[~data.index.duplicated(keep='first')]

    # Chuyển dữ liệu thành định dạng pivot để dễ xử lý dữ liệu bị thiếu
    data_model = data.pivot(index='Date', columns='Time', values=required_columns)

    print("Filling:")
    for index, row in data_model.iterrows():
        if pd.isnull(row).any():  # Kiểm tra nếu có giá trị nào bị thiếu trong hàng
            missing_times = row[pd.isnull(row)].index.tolist()  # Lấy danh sách các thời gian bị thiếu
            for time in missing_times:
                if isinstance(time, str):  # Đảm bảo 'time' là chuỗi
                    try:
                        index_date = datetime.strptime(index, "%Y-%m-%d").date()  # Chuyển chỉ mục thành ngày
                        time_of_day = datetime.strptime(time, "%H:%M:%S").time()  # Chuyển thời gian thành đối tượng time
                        if index_date <= datetime.now().date() and time_of_day <= datetime.now().time():
                            print(f"At {index} {time}")
                    except ValueError:
                        print(f"Invalid time format at {index} {time}")
                else:
                    print(f"Unexpected type for time at {index}: {type(time)}")

    # Lấy các hàng còn thiếu và tính tỷ lệ dòng bị thiếu
    filled_rows = data_model[data_model.isnull().any(axis=1)]
    filled_count = len(filled_rows)
    total_rows = len(data)
    fill_ratio = filled_count / total_rows

    if fill_ratio > 0.03:
        print("Warning: Tỷ lệ dòng đã được fill vượt quá 3%, có thể ảnh hưởng đến kết quả.")

    # Forward-fill và backward-fill các giá trị bị thiếu cho tất cả các cột
    data_model = data_model.ffill(axis=1).bfill(axis=1).stack().reset_index()

    # Điền các giá trị NaN còn lại
    data_model = data_model.fillna(method='ffill')

    # Lọc dữ liệu tương lai
    valid_index = np.all([data_model['Date'] == str(datetime.now().date()), data_model['Time'] <= str(datetime.now().time())], axis=0)
    valid_index = valid_index | (data_model['Date'] < str(datetime.now().date()))
    data_model = data_model[valid_index]

    return data_model