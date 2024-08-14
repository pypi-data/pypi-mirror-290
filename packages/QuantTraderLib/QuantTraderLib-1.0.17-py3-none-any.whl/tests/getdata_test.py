import pandas as pd
import datetime as dt
from QuantTraderLib.data.get_data import get_vn_index, get_vn_derivative, get_vnstock, get_crypto, get_forex, get_stock, get_vn30f_minute, get_forex_minute

def test_get_vn_index_input_types():
    # Kiểm tra loại dữ liệu của các tham số đầu vào
    assert isinstance(get_vn_index('VNINDEX', '2023-01-01'), pd.DataFrame)
    assert isinstance(get_vn_index('VNINDEX', dt.datetime(2023, 1, 1)), pd.DataFrame)
    assert isinstance(get_vn_index('VNINDEX', '2023-01-01', end_date='2023-01-10'), pd.DataFrame)
    assert isinstance(get_vn_index('VNINDEX', '2023-01-01', end_date=dt.datetime(2023, 1, 10)), pd.DataFrame)
    
def test_get_vn_derivative_input_types():
    # Kiểm tra loại dữ liệu của các tham số đầu vào
    assert isinstance(get_vn_derivative('VN30F1M', '2024-01-01'), pd.DataFrame)
    assert isinstance(get_vn_derivative('VN30F1M', dt.datetime(2024, 1, 1)), pd.DataFrame)
    assert isinstance(get_vn_derivative('VN30F1M', '2024-01-01', end_date='2024-01-10'), pd.DataFrame)
    assert isinstance(get_vn_derivative('VN30F1M', '2024-01-01', end_date=dt.datetime(2024, 1, 10)), pd.DataFrame)

def test_get_vnstock_input_types():
    # Kiểm tra loại dữ liệu của các tham số đầu vào
    assert isinstance(get_vnstock('VCB', '2023-01-01'), pd.DataFrame)
    assert isinstance(get_vnstock('VCB', dt.datetime(2023, 1, 1), '1D'), pd.DataFrame)
    today = dt.datetime.now()
    assert isinstance(get_vnstock('VCB', start_date=today-dt.timedelta(days=90), resolution='1H', end_date = today), pd.DataFrame)

def test_get_forex_input_types():
    # Kiểm tra loại dữ liệu của các tham số đầu vào
    assert isinstance(get_forex('EURUSD', '2023-01-01', '2023-01-10'), pd.DataFrame)
    assert isinstance(get_forex('EURUSD', dt.datetime(2023, 1, 1), dt.datetime(2023, 1, 10)), pd.DataFrame)

def test_get_crypto_input_types():
    # Kiểm tra loại dữ liệu của các tham số đầu vào
    assert isinstance(get_crypto('BTC-USD', start_date='2023-01-01'), pd.DataFrame)
    assert isinstance(get_crypto('BTC-USD', '2023-01-01', end_date='2023-01-10'), pd.DataFrame)
    assert isinstance(get_crypto('BTC-USD', '2023-01-01', end_date=dt.datetime(2023, 1, 10)), pd.DataFrame)

def test_get_stock_input_types():
    # Kiểm tra loại dữ liệu của các tham số đầu vào
    assert isinstance(get_stock('TSLA', '2024-01-01'), pd.DataFrame)
    assert isinstance(get_stock('TSLA', dt.datetime(2024, 1, 1)), pd.DataFrame)
    assert isinstance(get_stock('TSLA', '2024-01-01', end_date='2024-01-10'), pd.DataFrame)
    assert isinstance(get_stock('TSLA', '2024-01-01', end_date=dt.datetime(2024, 1, 10)), pd.DataFrame)

def test_get_vn30f1m_minute_input_types():
    # Kiểm tra loại dữ liệu của các tham số đầu vào
    assert isinstance(get_vn30f_minute('VN30F1M', '2023-07-01'), pd.DataFrame)
    assert isinstance(get_vn30f_minute('VN30F1M', dt.datetime(2023, 7, 1)), pd.DataFrame)
    assert isinstance(get_vn30f_minute('VN30F1M', '2023-07-01', end_date='2023-08-31'), pd.DataFrame)
    assert isinstance(get_vn30f_minute('VN30F1M', '2023-07-01', end_date=dt.datetime(2023, 8, 31)), pd.DataFrame)

def test_forex_data_minute_input_types():
    # Kiểm tra loại dữ liệu của các tham số đầu vào
    assert isinstance(get_forex_minute('EURUSD=X', period='1mo', interval='5m'), pd.DataFrame)
    assert isinstance(get_forex_minute('EURUSD=X', period='1mo'), pd.DataFrame)
    assert isinstance(get_forex_minute('EURUSD=X', interval='5m'), pd.DataFrame)
    assert isinstance(get_forex_minute('EURUSD=X'), pd.DataFrame)
