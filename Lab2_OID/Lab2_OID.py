import os
import time
import pandas as pd
import numpy as np

def generate_data(n_rows=1_000_000):
    print("Генерація тестових даних")
    np.random.seed(42)
    data = {
        'transaction_id': range(1, n_rows + 1),
        'user_id': np.random.randint(1000, 50000, size=n_rows),
        'amount': np.round(np.random.uniform(1.0, 5000.0, size=n_rows), 2),
        'category': np.random.choice(['Groceries', 'Electronics', 'Clothing', 'Travel', 'Utilities'], size=n_rows),
        'timestamp': pd.date_range(start='2026-01-01', periods=n_rows, freq='s')
    }
    df = pd.DataFrame(data)
    
    csv_file = 'transactions.csv'
    df.to_csv(csv_file, index=False)
    print(f"Файл {csv_file} успішно створено.\n")
    return df, csv_file

def convert_formats(df):
    print("Збереження у різні формати Parquet")
    
    files = {
        'CSV': 'transactions.csv',
        'Parquet (NONE)': 'transactions_none.parquet',
        'Parquet (SNAPPY)': 'transactions_snappy.parquet',
        'Parquet (GZIP)': 'transactions_gzip.parquet'
    }
    
    # Збереження
    df.to_parquet(files['Parquet (NONE)'], compression=None)
    df.to_parquet(files['Parquet (SNAPPY)'], compression='snappy')
    df.to_parquet(files['Parquet (GZIP)'], compression='gzip')
    
    # Вимірювання розмірів
    print("-" * 50)
    print(f"{'Формат':<20} | {'Розмір (MB)':<12} | {'Співвідношення':<12}")
    print("-" * 50)
    
    csv_size = os.path.getsize(files['CSV']) / (1024 * 1024)
    
    for name, path in files.items():
        size_mb = os.path.getsize(path) / (1024 * 1024)
        ratio = f"{size_mb / csv_size * 100:.1f}%"
        print(f"{name:<20} | {size_mb:<12.2f} | {ratio:<12}")
    print("-" * 50 + "\n")
    
    return files

def run_benchmark(files):
    print("Виконання тестового запиту (...")
    print("-" * 50)
    print(f"{'Формат':<20} | {'Час виконання (ms)':<20}")
    print("-" * 50)
    
    for name, path in files.items():
        start_time = time.perf_counter()
        
        if name == 'CSV':
            data = pd.read_csv(path, usecols=['category', 'amount'])
        else:
            data = pd.read_parquet(path, columns=['category', 'amount'])
            
        result = data.groupby('category')['amount'].sum()
        
        end_time = time.perf_counter()
        
        execution_time_ms = (end_time - start_time) * 1000
        print(f"{name:<20} | {execution_time_ms:<20.2f}")
        
    print("-" * 50)



df, csv_file = generate_data(n_rows=1_000_000)

files = convert_formats(df)

run_benchmark(files)