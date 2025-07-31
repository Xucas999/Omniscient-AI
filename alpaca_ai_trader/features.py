import pandas as pd

def make_features(df):
    df['ma5'] = df['close'].rolling(5).mean()
    df['ma10'] = df['close'].rolling(10).mean()
    df['volatility'] = df['return'].rolling(10).std()
    df = df.dropna()
    X = df[['ma5', 'ma10', 'volatility']].values
    y = df['label'].values
    return X, y, df
