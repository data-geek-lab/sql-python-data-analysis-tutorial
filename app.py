import streamlit as st
import pandas as pd
import plotly.express as px
from upload_handler import save_to_mysql
from mysql_config import get_connection

st.set_page_config(page_title="CSV to MySQL Dashboard", layout="wide")

st.title("📊 Upload CSV & Visualize Data with MySQL + Streamlit")

# Step 1: Upload CSV
st.subheader("📁 Step 1: Upload Your CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
    st.dataframe(df.head())

    if st.button("💾 Save to MySQL"):
        try:
            save_to_mysql(df, "uploaded_data")
            st.success("✅ Data saved to MySQL as 'uploaded_data' table.")
        except Exception as e:
            st.error(f"❌ Error saving to MySQL: {e}")

# Step 2: Load Data from MySQL
st.subheader("📥 Step 2: Load Data from MySQL")

if "loaded_df" not in st.session_state:
    st.session_state.loaded_df = None

if st.button("🔄 Load Data"):
    try:
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM uploaded_data", conn)
        conn.close()
        st.session_state.loaded_df = df
        st.success("✅ Data loaded from MySQL!")
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")

# Step 3: Visualize the Data
st.subheader("📈 Step 3: Visualize Your Data")

if st.session_state.loaded_df is not None:
    df = st.session_state.loaded_df

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    all_cols = df.columns.tolist()

    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("Choose X-axis", options=all_cols, key="x_axis")
    with col2:
        y_axis = st.selectbox("Choose Y-axis (numeric only)", options=numeric_cols, key="y_axis")

    if x_axis and y_axis:
        fig = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("ℹ️ Please load data first using the button above.")
