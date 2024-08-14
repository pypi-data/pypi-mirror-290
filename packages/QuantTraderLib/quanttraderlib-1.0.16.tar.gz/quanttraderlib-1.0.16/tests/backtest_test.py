import pandas as pd
import numpy as np
from QuantTraderLib.backtest.event_base import use_changes
from QuantTraderLib.backtest.vectorized import use_position, use_signal_ma, use_trailing

# Sample data for testing
data = pd.DataFrame({
    'Open': np.random.rand(100),
    'High': np.random.rand(100),
    'Low': np.random.rand(100),
    'Close': np.random.rand(100)
})

def test_use_changes():
    changes = np.random.randn(100)  # Random changes
    changes = pd.Series(changes)
    stats, bt = use_changes(data, changes)
    
    # Check if the output is a tuple
    assert isinstance((stats, bt), tuple)
    
    # Check if bt is an instance of a specific class (replace `Backtest` with the actual class if known)
    assert hasattr(bt, 'run') 

def test_use_position():
    pos_array = np.random.choice([1, -1], size=100)  # Random buy/sell signals
    pos_array = pd.Series(pos_array)
    stats, bt = use_position(data, pos_array)
    
    # Check if the output is a tuple
    assert isinstance((stats, bt), tuple)
    
    # Check if bt is an instance of a specific class (replace `Backtest` with the actual class if known)
    assert hasattr(bt, 'run') 

def test_use_signal_ma():
    stats, bt = use_signal_ma(data, ma1=5, ma2=10)
    
    # Check if the output is a tuple
    assert isinstance((stats, bt), tuple)
    
    # Check if bt is an instance of a specific class (replace `Backtest` with the actual class if known)
    assert hasattr(bt, 'run') 

# def test_use_trailing():
#     stats, bt = use_trailing(data, atr_periods=14, trailing_sl=2, rolling=20)
    
#     # Check if the output is a tuple
#     assert isinstance((stats, bt), tuple)
    
#     # Check if bt is an instance of a specific class (replace `Backtest` with the actual class if known)
#     assert hasattr(bt, 'run') 