import pandas as pd
import numpy as np
from QuantTraderLib.backtest.event_base import use_changes
from QuantTraderLib.backtest.vectorized import use_position, use_signal_ma, use_trailing
from QuantTraderLib.backtest.pnl import check_positions, calculate_pnl
from QuantTraderLib._backtest_source.source import Backtest
from QuantTraderLib.data.get_data import get_vn30f_minute

#Test pnl.py
def test_check_positions():
    """Kiểm tra loại dữ liệu của đầu ra hàm check_positions"""
    df = pd.DataFrame({
        'close': [100, 101, 102, 103, 104, 105],
        'position': [1, 0, 0, -1, 0, 0]
    }, index=pd.date_range(start='2023-01-01', periods=6, freq='B'))
    
    valid_positions = check_positions(df)
    
    # Kiểm tra loại dữ liệu của đầu ra
    assert isinstance(valid_positions, list)
    assert all(isinstance(pos, tuple) and len(pos) == 2 for pos in valid_positions)

def test_calculate_pnl():
    """Kiểm tra loại dữ liệu của đầu ra hàm calculate_pnl"""
    df = pd.DataFrame({
        'close': [100, 101, 102, 103, 104, 105],
        'position': [1, 0, 0, -1, 0, 0]
    }, index=pd.date_range(start='2023-01-01', periods=6, freq='B'))
    
    pnl, valid_positions = calculate_pnl(df)
    
    # Kiểm tra loại dữ liệu của đầu ra
    assert isinstance(pnl, np.ndarray) or pnl is None
    assert isinstance(valid_positions, list)
    assert all(isinstance(pos, tuple) and len(pos) == 2 for pos in valid_positions) if valid_positions else True


# Test event_base.py and vectorized.py
data = get_vn30f_minute('VN30F1M', '2023-07-01')

def test_use_changes():
    changes = np.random.randn(data.shape[0])  # Random changes
    changes = pd.Series(changes)
    stats, bt = use_changes(data, changes)
    
    # Check if the output is a tuple
    assert isinstance((stats, bt), tuple)
    
    assert isinstance(bt, Backtest)
    assert hasattr(bt, 'run') 

def test_use_position():
    pos_array = np.random.choice([1, -1], size=data.shape[0])  # Random buy/sell signals
    pos_array = pd.Series(pos_array)
    stats, bt = use_position(data, pos_array)
    
    # Check if the output is a tuple
    assert isinstance((stats, bt), tuple)
    
    assert isinstance(bt, Backtest)
    assert hasattr(bt, 'run') 

def test_use_signal_ma():
    stats, bt = use_signal_ma(data, ma1=5, ma2=10)
    
    # Check if the output is a tuple
    assert isinstance((stats, bt), tuple)
    
    assert isinstance(bt, Backtest)
    assert hasattr(bt, 'run') 

def test_use_trailing():
    # stats, bt = use_trailing(data, atr_periods=14, trailing_sl=2, rolling=20)
    stats, bt = use_trailing(data=data, atr_periods=40, trailing_sl=3, rolling=10)
    # Check if the output is a tuple
    assert isinstance((stats, bt), tuple)
    
    assert isinstance(bt, Backtest)
    assert hasattr(bt, 'run') 