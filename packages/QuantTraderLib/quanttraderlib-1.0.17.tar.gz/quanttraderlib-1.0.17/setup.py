from setuptools import setup, find_packages

setup(
    name='QuantTraderLib',
    version='1.0.17',
    author='Hephaestus Tech',
    author_email='heptech2023@gmail.com',
    description='QuantTraderLib là một thư viện Python hỗ trợ những vấn đề về quant trading.',
    url='https://github.com/Gnosis-Tech/PyQuantTrader_Dev',  # Project homepage URL
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'QuantTraderLib._backtest_source': ['autoscale_cb.js'],  # Update to the correct path
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    # giống với requirements, các thư viện sau sẽ tự cài đặt khi pip install QuantTraderLib
    install_requires=[
        'numpy==2.0.1',
        'yfinance==0.2.41',
        'vnstock==0.2.9.2.2',
        'pandas==2.2.2',
        'pandas_datareader==0.10.0',
        'bokeh==3.4.3',
        'backtesting==0.3.3',
        'lunardate==0.2.2',
        'seaborn==0.13.2',
        'scikit-learn==1.5.1',
    ],
    python_requires='>=3.7, <3.11',
)
