import streamlit as st
import pandas as pd
import datetime
import os

# 保存ファイルのパス
FILE_PATH = "products.csv"

# 初期化処理（ファイルがなければ作成）
if not os.path.exists(FILE_PATH):
    df_init = pd.DataFrame(columns=["name", "expiry", "quantity"])
    df_init.to_csv(FILE_PATH, index=False)

# CSVの読み込み
df = pd.read_csv(FILE_PATH)
df["expiry"] = pd.to_datetime(df["expiry"], errors='coerce')

# ヘッダー
st.title("賞味期限管理アプリ（共有用）")

# タブ切り替え
tab_all, tab_frequent = st.tabs(["すべての商品", "よく使う商品"])

# 入力フォーム
with st.form("product_form"):
    st.subheader("商品を追加")
    name = st.text_input("商品名")
    expiry = st.date_input("賞味期限", datetime.date.today())
    quantity = st.number_input("数量", min_value=1, value=1, step=1)
    submitted = st.form_submit_button("追加")

    if submitted:
        new_row = pd.DataFrame({
            "name": [name],
            "expiry": [str(expiry)],  # 保存前に文字列に変換
            "quantity": [quantity]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(FILE_PATH, index=False)
        st.success("商品を追加しました！")

# 共通関数：期限表示のスタイル
def color_row(row):
    today = pd.Timestamp.today().normalize()
    if pd.isnull(row["expiry"]):
        return [""] * len(row)
    days_left = (row["expiry"] - today).days
    if days_left < 0:
        return ["background-color: lightcoral"] * len(row)
    elif days_left <= 2:
        return ["background-color: khaki"] * len(row)
    return [""] * len(row)

# テーブルの表示（すべてのタブ）
with tab_all:
    st.subheader("すべての商品")
    if not df.empty:
        df["expiry"] = pd.to_datetime(df["expiry"], errors='coerce')
        styled = df.style.apply(color_row, axis=1)
        st.dataframe(styled, use_container_width=True)
    else:
        st.info("まだ商品が登録されていません。")
