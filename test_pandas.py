import pandas as pd

# サンプルデータ（辞書型）
data = {
    'ASIN': ['A123', 'B234', 'C345'],
    '商品名': ['商品A', '商品B', '商品C'],
    '売上個数': [10, 20, 15],
    '売上金額': [5000, 10000, 7500]
}

# pandas データフレームに変換
df = pd.DataFrame(data)

# データ表示
print(df)

# CSVに保存（同じフォルダ内に test_output.csv が作られます）
df.to_csv('test_output.csv', index=False, encoding='utf-8-sig')
