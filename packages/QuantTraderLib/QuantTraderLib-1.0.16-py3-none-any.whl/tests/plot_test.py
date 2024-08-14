# import pandas as pd
# import numpy as np
# import pytest
# from datetime import datetime, date
# from QuantTraderLib.plot.plot import Isolation_Forest, IQR, Multivariate_Density, Seasonal_Decomposition, MAD

# def test_Multivariate_Density():
#     # Tạo dữ liệu giả
#     np.random.seed(0)
#     data = pd.DataFrame({
#         'A': np.random.randn(100),
#         'B': np.random.randn(100),
#         'C': np.random.randn(100),
#         'D': np.random.randn(100),
#         'E': np.random.randn(100),
#         'F': np.random.randn(100)
#     })
    
#     # Kiểm thử với features được chỉ định
#     try:
#         Multivariate_Density(data, features=['A', 'B', 'C'])
#     except Exception as e:
#         pytest.fail(f"Multivariate_Density failed with specified features: {e}")
    
#     # Kiểm thử với features ngẫu nhiên
#     try:
#         Multivariate_Density(data)
#     except Exception as e:
#         pytest.fail(f"Multivariate_Density failed with random features: {e}")

# def test_Isolation_Forest():
#     # Tạo dữ liệu giả
#     np.random.seed(0)
#     data = pd.Series(np.random.randn(100))
    
#     # Kiểm thử với các tham số mặc định
#     fig, ax = Isolation_Forest(data)
#     assert fig is not None
#     assert ax is not None
    
#     # Kiểm thử với tham số khác
#     fig, ax = Isolation_Forest(data, contamination=0.05, figure_size=(12, 10))
#     assert fig is not None
#     assert ax is not None

# def test_IQR():
#     # Tạo dữ liệu giả
#     np.random.seed(0)
#     data = pd.Series(np.random.randn(100))
    
#     # Kiểm thử với các tham số mặc định
#     fig, ax = IQR(data)
#     assert fig is not None
#     assert ax is not None
    
#     # Kiểm thử với tham số khác
#     fig, ax = IQR(data, threshold=2.0, figure_size=(12, 10))
#     assert fig is not None
#     assert ax is not None

# def test_MAD():
#     # Tạo dữ liệu giả
#     np.random.seed(0)
#     data = pd.Series(np.random.randn(100))
    
#     # Kiểm thử với các tham số mặc định
#     fig, ax = MAD(data)
#     assert fig is not None
#     assert ax is not None
    
#     # Kiểm thử với tham số khác
#     fig, ax = MAD(data, threshold=4.0, figsize=(12, 10))
#     assert fig is not None
#     assert ax is not None

# def test_Seasonal_Decomposition():
#     # Tạo dữ liệu giả với mùa vụ
#     np.random.seed(0)
#     data = pd.Series(np.sin(np.linspace(0, 20, 100)) + np.random.normal(size=100))
    
#     # Kiểm thử với các tham số mặc định
#     Seasonal_Decomposition(data)
    
#     # Kiểm thử với tham số khác
#     Seasonal_Decomposition(data, model='multiplicative', period=20)

#     # Kiểm tra xem hàm có thực thi mà không gây lỗi
#     try:
#         Seasonal_Decomposition(data)
#         Seasonal_Decomposition(data, model='multiplicative', period=20)
#     except Exception as e:
#         pytest.fail(f"Seasonal_Decomposition failed with error: {e}")