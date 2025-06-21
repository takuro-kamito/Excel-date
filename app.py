import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="売上比較ダッシュボード", layout="wide")
st.title("📊 売上比較ダッシュボード")

# 1) ファイルアップロード
uploaded = st.file_uploader("Excelファイルをアップロードしてください", type=["xlsx"])
if not uploaded:
    st.info("まずはファイルをアップロードしてください。")
    st.stop()

# 2) シート選択
xls = pd.ExcelFile(uploaded)
sheets = xls.sheet_names
prev_sheet = st.sidebar.selectbox("前月シートを選択", sheets)
cur_sheet  = st.sidebar.selectbox("当月シートを選択", sheets, index=min(1, len(sheets)-1))

# 3) データ読み込み & Unnamed 列排除
df_prev = pd.read_excel(uploaded, sheet_name=prev_sheet)
df_cur  = pd.read_excel(uploaded, sheet_name=cur_sheet)
df_prev = df_prev.loc[:, [not str(c).startswith("Unnamed") for c in df_prev.columns]]
df_cur  = df_cur.loc[:,  [not str(c).startswith("Unnamed") for c in df_cur.columns]]

# 4) カラムを絞って選択
# ― カテゴリ列：object 型のみ
cat_cols = [c for c in df_cur.columns if df_cur[c].dtype == "object"]
# ― 数値列：数値型のみ
num_cols = [c for c in df_cur.columns if pd.api.types.is_numeric_dtype(df_cur[c])]

if not cat_cols or not num_cols:
    st.error("カテゴリ列（文字列型）または数値列（数値型）が検出できません。")
    st.stop()

sel_cat   = st.sidebar.selectbox("カテゴリ列を選択",   cat_cols)
sel_sales = st.sidebar.selectbox("売上列を選択",       num_cols)

cat_col   = sel_cat
sales_col = sel_sales

# 5) 数値変換＆チェック
df_prev[sales_col] = pd.to_numeric(df_prev[sales_col], errors="coerce")
df_cur [sales_col] = pd.to_numeric(df_cur [sales_col], errors="coerce")

if df_cur[sales_col].dropna().empty:
    st.error(f"列「{sales_col}」に数値データがありません。別の列を選択してください。")
    st.stop()

# 6) 集計＆比較
agg_prev   = df_prev.groupby(cat_col)[sales_col].sum().rename("前月売上")
agg_cur    = df_cur .groupby(cat_col)[sales_col].sum().rename("当月売上")
comparison = pd.concat([agg_prev, agg_cur], axis=1).fillna(0)

# 7) 伸び率計算（必ず float 型に変換）
comparison["伸び率(%)"] = (
    (comparison["当月売上"] - comparison["前月売上"]) 
    / comparison["前月売上"].replace(0, pd.NA) * 100
).astype(float).round(1)

# 8) グラフ描画
st.subheader("📈 カテゴリ別 売上比較")
fig, ax = plt.subplots(figsize=(8, max(4, len(comparison)*0.5)))
comparison[["前月売上","当月売上"]].plot(kind="bar", ax=ax)
ax.set_ylabel("売上額")
ax.legend(loc="upper left")
st.pyplot(fig)

# 9) テーブル表示
st.subheader("📋 比較結果一覧")
st.table(comparison)
