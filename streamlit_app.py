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
            "expiry": [expiry],
            "quantity": [quantity]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(FILE_PATH, index=False)
        st.success("商品を追加しました！")

# 共通関数：期限表示
def render_table(filtered_df):
    today = datetime.datetime.today()

    def color_row(row):
        days_left = (row["expiry"] - today).days
        if days_left < 0:
            return ['background-color: #FFCCCC'] * len(row)
        elif days_left <= 2:
            return ['background-color: #FFF0B3'] * len(row)
        else:
            return [''] * len(row)

    styled = filtered_df.style.apply(color_row, axis=1)
    st.dataframe(styled, use_container_width=True)

# すべての商品タブ
with tab_all:
    st.subheader("すべての商品")
    if not df.empty:
        if st.button("古い順に並び替え"):
            df = df.sort_values("expiry")
        render_table(df)

        delete_index = st.number_input(
            "削除したい行番号（0〜）", min_value=0, max_value=len(df)-1, step=1
        )
        if st.button("指定した行を削除"):
            df = df.drop(index=delete_index).reset_index(drop=True)
            df.to_csv(FILE_PATH, index=False)
            st.success("削除しました")
            # st.experimental_rerun()  ← コメントアウト

    else:
        st.info("まだ商品が登録されていません。")

# よく使う商品タブ
with tab_frequent:
    st.subheader("よく使う商品")
    common_items = df["name"].value_counts()
    frequent_names = common_items[common_items >= 3].index.tolist()
    filtered = df[df["name"].isin(frequent_names)]

    if not filtered.empty:
        render_table(filtered)
    else:
        st.info("よく使う商品はまだありません（3回以上追加で表示されます）")
