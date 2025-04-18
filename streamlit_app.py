import streamlit as st
import pandas as pd
import datetime
import os

# 保存ファイルのパス
FILE_PATH = "products.csv"

# 初期化（CSVファイルがない場合は作成）
if not os.path.exists(FILE_PATH):
    df_init = pd.DataFrame(columns=["name", "expiry", "quantity"])
    df_init.to_csv(FILE_PATH, index=False)

# CSVの読み込み
df = pd.read_csv(FILE_PATH)
df["expiry"] = pd.to_datetime(df["expiry"], errors="coerce")

st.title("賞味期限管理アプリ（簡易版）")

# 入力フォーム
with st.form("add_form"):
    name = st.text_input("商品名")
    expiry = st.date_input("賞味期限", datetime.date.today())
    quantity = st.number_input("数量", min_value=1, value=1)
    submitted = st.form_submit_button("追加")

    if submitted and name:
        new_row = pd.DataFrame({
            "name": [name],
            "expiry": [expiry],
            "quantity": [quantity]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(FILE_PATH, index=False)
        st.success("商品を追加しました！")
        st.experimental_rerun()

# 商品一覧表示
st.subheader("登録された商品一覧")
if df.empty:
    st.info("商品がまだ登録されていません。")
else:
    df_sorted = df.sort_values("expiry")
    st.dataframe(df_sorted, use_container_width=True)

    delete_index = st.number_input("削除する行番号（0〜）", min_value=0, max_value=len(df_sorted)-1, step=1)
    if st.button("削除"):
        df = df.drop(index=delete_index).reset_index(drop=True)
        df.to_csv(FILE_PATH, index=False)
        st.success("削除しました")
        st.experimental_rerun()
