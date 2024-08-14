import datetime as dt
import yfinance as yfin
import pandas as pd
from vnstock import stock_historical_data
import requests

# __all__ = ['get_vn_index', 'get_vn_derivative', 'get_vnstock', 'get_crypto', 'get_forex', 'get_stock', 'get_vn30f_minute', 'get_forex_minute']

def get_vn_index(symbol, start_date, resolution='1D', end_date=None):
    """
    Truy xuất dữ liệu lịch sử của chỉ số VN từ thị trường chứng khoán Việt Nam.

    Tham số:
        symbol (str): Ký hiệu của chỉ số VN.
        start_date (str hoặc datetime): Ngày bắt đầu cho dữ liệu lịch sử. Định dạng: 'YYYY-MM-DD'.
        resolution (str, tùy chọn): Độ phân giải của dữ liệu. Ví dụ: '1D' cho hàng ngày. Mặc định là '1D'.
        end_date (str hoặc datetime, tùy chọn): Ngày kết thúc cho dữ liệu lịch sử. Nếu không được cung cấp, mặc định là ngày hiện tại.

    Trả về:
        pandas.DataFrame: DataFrame chứa dữ liệu lịch sử của chỉ số VN với các cột 'Date', 'Open', 'High', 'Low', 'Close'.
    """
    if end_date is None:
        end_date = dt.datetime.now()
    df = stock_historical_data(symbol=symbol,
                            start_date=str(start_date)[0:10],
                            end_date=str(end_date)[0:10], resolution=resolution, type='index', beautify=False, decor=False, source='DNSE')
    if 'time' in df.columns:
        df.rename(columns={'time': 'Date', 'open': 'Open', 'high':'High', 'low':'Low', 'close':'Close',}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])

    # Chỉ giữ lại các cột OHLC
    ohlc_columns = ['Date', 'Open', 'High', 'Low', 'Close']
    df = df[ohlc_columns]
    return df

def get_vn_derivative(symbol, start_date, resolution='1D', end_date=None):
    """
    Truy xuất dữ liệu lịch sử của các hợp đồng phái sinh VN từ thị trường chứng khoán Việt Nam.

    Tham số:
        symbol (str): Ký hiệu của hợp đồng phái sinh VN.
        start_date (str hoặc datetime): Ngày bắt đầu cho dữ liệu lịch sử. Định dạng: 'YYYY-MM-DD'.
        resolution (str, tùy chọn): Độ phân giải của dữ liệu. Ví dụ: '1D' cho hàng ngày. Mặc định là '1D'.
        end_date (str hoặc datetime, tùy chọn): Ngày kết thúc cho dữ liệu lịch sử. Nếu không được cung cấp, mặc định là ngày hiện tại.

    Trả về:
        pandas.DataFrame: DataFrame chứa dữ liệu lịch sử của các hợp đồng phái sinh VN với các cột 'Date', 'Open', 'High', 'Low', 'Close'.
    """
    if end_date is None:
        end_date = dt.datetime.now()
    df = stock_historical_data(symbol=symbol,
                            start_date=str(start_date)[0:10],
                            end_date=str(end_date)[0:10], resolution=resolution, type='derivative', beautify=False, decor=False, source='DNSE')
    if 'time' in df.columns:
        df.rename(columns={'time': 'Date', 'open': 'Open', 'high':'High', 'low':'Low', 'close':'Close',}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])

    # Chỉ giữ lại các cột OHLC
    ohlc_columns = ['Date', 'Open', 'High', 'Low', 'Close']
    df = df[ohlc_columns]
    return df

def get_vnstock(symbol, start_date, resolution='1D', end_date=None):
    """
    Truy xuất dữ liệu lịch sử của cổ phiếu VN từ thị trường chứng khoán Việt Nam.

    Tham số:
        symbol (str): Ký hiệu của cổ phiếu VN.
        start_date (str hoặc datetime): Ngày bắt đầu cho dữ liệu lịch sử. Định dạng: 'YYYY-MM-DD'.
        resolution (str, tùy chọn): Độ phân giải của dữ liệu. Ví dụ: '1D' cho hàng ngày. Mặc định là '1D'.
        end_date (str hoặc datetime, tùy chọn): Ngày kết thúc cho dữ liệu lịch sử. Nếu không được cung cấp, mặc định là ngày hiện tại.

    Trả về:
        pandas.DataFrame: DataFrame chứa dữ liệu lịch sử của cổ phiếu VN với các cột 'Date', 'Open', 'High', 'Low', 'Close'.
    """
    if end_date is None:
        end_date = dt.datetime.now() 
    df = None
    df = stock_historical_data(symbol=symbol,
                               start_date=str(start_date)[0:10],
                               end_date=str(end_date)[0:10], resolution=resolution, type='stock', beautify=False, decor=False, source='DNSE')
    if 'time' in df.columns:
        df.rename(columns={'time': 'Date', 'open': 'Open', 'high':'High', 'low':'Low', 'close':'Close'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])

    # Chỉ giữ lại các cột OHLC
    ohlc_columns = ['Date', 'Open', 'High', 'Low', 'Close']
    df = df[ohlc_columns]
    return df

def get_forex(symbol, start_date, end_date=None):
    """
    Truy xuất dữ liệu lịch sử cho một cặp tiền từ Yahoo Finance.

    Tham số:
        symbol (str): Ký hiệu của cặp tiền. Ví dụ: 'EURUSD'.
        start_date (str hoặc datetime): Ngày bắt đầu cho dữ liệu lịch sử. Định dạng: 'YYYY-MM-DD'.
        end_date (str hoặc datetime, tùy chọn): Ngày kết thúc cho dữ liệu lịch sử. Nếu không được cung cấp, mặc định là ngày hiện tại.

    Trả về:
        pandas.DataFrame: DataFrame chứa dữ liệu lịch sử của cặp tiền với các cột 'Date', 'Open', 'High', 'Low', 'Close'.
    """
    if end_date is None:
        end_date = dt.datetime.now()
    forex_data = yfin.download(symbol, start=start_date, end=end_date)

    # Đặt lại index thành cột 'Date' và chuyển đổi thành pd.Datetime
    forex_data.index = pd.to_datetime(forex_data.index)
    forex_data.reset_index(inplace=True)
    forex_data['Date'] = pd.to_datetime(forex_data['Date']).dt.date

    # Chỉ giữ lại các cột OHLC
    ohlc_columns = ['Date', 'Open', 'High', 'Low', 'Close']
    forex_data = forex_data[ohlc_columns]

    return forex_data

def get_crypto(crypto_currency, start_date, end_date=None):
    """
    Truy xuất dữ liệu lịch sử cho một loại tiền điện tử cụ thể trong đơn vị USD từ Yahoo Finance.

    Tham số:
        crypto_currency (str): Ký hiệu hoặc tên của tiền điện tử. Ví dụ: 'BTC-USD'.
        start_date (str hoặc datetime): Ngày bắt đầu cho dữ liệu lịch sử. Định dạng: 'YYYY-MM-DD'.
        end_date (str hoặc datetime, tùy chọn): Ngày kết thúc cho dữ liệu lịch sử. Nếu không được cung cấp, mặc định là ngày hiện tại.

    Trả về:
        pandas.DataFrame: DataFrame chứa dữ liệu lịch sử của tiền điện tử với các cột 'Date', 'Open', 'High', 'Low', 'Close'.
    """
    if end_date is None:
        end_date = dt.datetime.now()
    df = yfin.download(crypto_currency, start=start_date, end=end_date)

    # Đặt lại index thành cột 'Date' và chuyển đổi thành pd.Datetime
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    # Chỉ giữ lại các cột OHLC
    ohlc_columns = ['Date', 'Open', 'High', 'Low', 'Close']
    df = df[ohlc_columns]

    return df

def get_stock(symbol, start_date, end_date=None):
    """
    Truy xuất dữ liệu lịch sử của cổ phiếu từ Yahoo Finance với khoảng thời gian cụ thể.

    Tham số:
        symbol (str): Ký hiệu của cổ phiếu. Ví dụ: 'AAPL'.
        start (str hoặc datetime): Ngày bắt đầu cho dữ liệu lịch sử. Định dạng: 'YYYY-MM-DD'.
        end (str hoặc datetime, tùy chọn): Ngày kết thúc cho dữ liệu lịch sử. Nếu không được cung cấp, mặc định là ngày hiện tại.

    Trả về:
        pandas.DataFrame: DataFrame chứa dữ liệu lịch sử của cổ phiếu với các cột 'Date', 'Open', 'High', 'Low', 'Close'.
    """
    ticker = yfin.Ticker(symbol)
    now = dt.datetime.now().strftime("%Y-%m-%d")
    if end_date is None:
        end_date = dt.datetime.now()
    todays_data = ticker.history(period='1d', start=start_date, end=end_date)

    # Đặt lại index thành cột 'Date' và chuyển đổi thành pd.Datetime
    todays_data.reset_index(inplace=True)
    todays_data['Date'] = pd.to_datetime(todays_data['Date']).dt.date

    # Chỉ giữ lại các cột OHLC
    ohlc_columns = ['Date', 'Open', 'High', 'Low', 'Close']
    todays_data = todays_data[ohlc_columns]

    return todays_data

def get_vn30f_minute(symbol, start_date, end_date=None):
    """
    Truy xuất dữ liệu theo từng phút cho hợp đồng VN30F1M từ dịch vụ EnTrade.

    Tham số:
        symbol (str): Ký hiệu của hợp đồng VN30F1M.
        start_date (str hoặc datetime): Ngày bắt đầu cho dữ liệu lịch sử. Định dạng: 'YYYY-MM-DD'.
        end_date (str hoặc datetime, tùy chọn): Ngày kết thúc cho dữ liệu lịch sử. Nếu không được cung cấp, mặc định là thời điểm hiện tại.

    Trả về:
        pandas.DataFrame: DataFrame chứa dữ liệu lịch sử theo từng phút với các cột 'Date', 'Open', 'High', 'Low', 'Close', 'Volume'.
    """
    # Chuyển đổi start_date thành datetime nếu nó là chuỗi
    if isinstance(start_date, str):
        start_date = dt.datetime.strptime(start_date, '%Y-%m-%d')
    
    # Chuyển đổi start_date thành timestamp
    start_time = int((start_date - dt.timedelta(hours=7)).timestamp())

    # Chuyển đổi end_date thành datetime nếu nó là chuỗi, nếu không, dùng end_date như đã cung cấp
    if end_date:
        if isinstance(end_date, str):
            end_date = dt.datetime.strptime(end_date, '%Y-%m-%d')
        end_time = int((end_date - dt.timedelta(hours=7)).timestamp())
    else:
        end_time = 9999999999  # Một thời điểm trong tương lai để lấy dữ liệu đến hiện tại

    # Hàm truy xuất dữ liệu từ dịch vụ EnTrade
    def vn30f():
        return requests.get(f"https://services.entrade.com.vn/chart-api/chart?from={start_time}&resolution=1&symbol={symbol}&to={end_time}").json()
    
    # Tạo DataFrame từ dữ liệu truy xuất
    vn30fm = pd.DataFrame(vn30f()).iloc[:, :6]
    vn30fm['t'] = vn30fm['t'].astype(int).apply(lambda x: dt.datetime.utcfromtimestamp(x) + dt.timedelta(hours=7))
    vn30fm.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    
    # Chuyển đổi start_time và end_time thành datetime để in thông báo
    dt_object = dt.datetime.utcfromtimestamp(start_time) + dt.timedelta(hours=7)
    now_object = dt.datetime.utcfromtimestamp(end_time) + dt.timedelta(hours=7)

    print(f'===> Data {symbol} from {dt_object} to {now_object} has been appended ')
    
    # Chỉ giữ lại các cột OHLC
    ohlc_columns = ['Date', 'Open', 'High', 'Low', 'Close']
    return vn30fm[ohlc_columns]

def get_forex_minute(symbol, period='1d', interval='5m'):
    """
    Truy xuất dữ liệu theo từng phút cho một cặp tiền từ Yahoo Finance.

    Tham số:
        symbol (str): Ký hiệu của cặp tiền. Ví dụ: 'EURUSD'.
        period (str, tùy chọn): Khoảng thời gian dữ liệu. Mặc định là '1d'.
        interval (str, tùy chọn): Khoảng thời gian giữa các bản ghi. Mặc định là '5m'.

    Trả về:
        pandas.DataFrame: DataFrame chứa dữ liệu theo từng phút với các cột 'Date', 'Close'.
    """
    forex_data_minute = yfin.download(symbol, period=period, interval=interval)

    # Đặt lại index thành cột 'Date' và chuyển đổi thành pd.Datetime
    forex_data_minute.index = pd.to_datetime(forex_data_minute.index)
    forex_data_minute.reset_index(inplace=True)
    forex_data_minute['Date'] = pd.to_datetime(forex_data_minute['Datetime']).dt.tz_localize(None)

    # Thêm 6 giờ vào cột 'Date'
    forex_data_minute['Date'] = forex_data_minute['Date'] + pd.to_timedelta('6h')

    # Chỉ giữ lại OHLC
    ohlc_columns = ['Date', 'Open', 'High', 'Low', 'Close']
    forex_data_minute = forex_data_minute[ohlc_columns]

    # Trả về dữ liệu
    return forex_data_minute