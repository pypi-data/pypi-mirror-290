import pandas as pd
from datetime import datetime, date
from QuantTraderLib.data.clean_data import get_vietnam_trading_days, check_missing_trading_dates, fill_missing_days, check_missing_minutes, fill_missing_minutes

def test_get_vietnam_trading_days():
    # Kiểm tra loại dữ liệu đầu vào và đầu ra
    assert isinstance(get_vietnam_trading_days('2023-01-01', '2023-01-31'), list)
    assert isinstance(get_vietnam_trading_days(datetime(2023, 1, 1), datetime(2023, 1, 31)), list)
    assert all(isinstance(day, pd.Timestamp) for day in get_vietnam_trading_days('2023-01-01', '2023-01-31'))

def test_check_missing_trading_dates():
    # Tạo DataFrame mẫu
    df = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', end='2023-01-10'),
        'Value': range(10)
    })
    df_missing = check_missing_trading_dates(df)
    
    # Kiểm tra đầu ra
    assert isinstance(df_missing, pd.DataFrame)
    assert 'Date' in df_missing.columns
    assert df_missing['Date'].dtype == 'datetime64[ns]'

def test_fill_missing_days():
    # Tạo DataFrame mẫu
    df = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', end='2023-01-10'),
        'Open': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'Close': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    })
    df_filled = fill_missing_days(df)
    
    # Kiểm tra đầu ra
    assert isinstance(df_filled, pd.DataFrame)
    assert 'Date' in df_filled.columns
    assert df_filled['Date'].dtype == 'datetime64[ns]'

def test_check_missing_minutes():
    # Tạo DataFrame mẫu
    now = datetime.now()
    df = pd.DataFrame({
        'Date': [now.date()] * 60,
        'Time': [now.replace(minute=i).time() for i in range(60)],
        'Value': range(60)
    })
    missing_minutes = check_missing_minutes(df)
    
    # Kiểm tra đầu ra
    assert isinstance(missing_minutes, dict)
    assert all(isinstance(day, date) for day in missing_minutes.keys())
    # assert all(isinstance(key, date) for key in missing_minutes.keys())
    assert all(isinstance(minute, str) for minutes in missing_minutes.values() for minute in minutes)

def test_fill_missing_minutes():
    # Tạo DataFrame mẫu
    now = datetime.now()
    df = pd.DataFrame({
        'Date': [now.date()] * 60,
        'Time': [now.replace(minute=i).time() for i in range(60)],
        'Value': range(60)
    })
    
    missing_times_per_day = check_missing_minutes(df)
    df_filled = fill_missing_minutes(df, missing_times_per_day)
    
    # Kiểm tra đầu ra
    assert isinstance(df_filled, pd.DataFrame)
    assert 'Date' in df_filled.columns
    assert 'Time' in df_filled.columns
    assert df_filled['Date'].dtype == 'object'
    assert df_filled['Time'].dtype == 'object'


