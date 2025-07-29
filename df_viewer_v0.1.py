import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#---------------------------------------------------------------------------------------------------------------------------------
### Title for your Streamlit app
#---------------------------------------------------------------------------------------------------------------------------------
#import custom_style()
st.set_page_config(page_title="Data Explorer Studio | v0.1",
                   layout="wide",
                   page_icon="💻",              
                   initial_sidebar_state="auto")
#---------------------------------------------------------------------------------------------------------------------------------
### CSS
#---------------------------------------------------------------------------------------------------------------------------------
st.markdown(
        """
        <style>
        .centered-info {display: flex; justify-content: center; align-items: center; 
                        font-weight: bold; font-size: 15px; color: #007BFF; 
                        padding: 5px; background-color: #FFFFFF;  border-radius: 5px; border: 1px solid #007BFF;
                        margin-top: 0px;margin-bottom: 5px;}
        .stMarkdown {margin-top: 0px !important; padding-top: 0px !important;}                       
        </style>
        """,unsafe_allow_html=True,)

#---------------------------------------------------------------------------------------------------------------------------------
### Description for your Streamlit app
#---------------------------------------------------------------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .title-large {
        text-align: center;
        font-size: 35px;
        font-weight: bold;
        background: linear-gradient(to left, red, orange, blue, indigo, violet);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .title-small {
        text-align: center;
        font-size: 20px;
        background: linear-gradient(to left, red, orange, blue, indigo, violet);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    <div class="title-large">Data Explorer Studio</div>
    <div class="title-small">Version : 0.1</div>
    """,
    unsafe_allow_html=True
)

#----------------------------------------
st.markdown('<div class="centered-info"><span style="margin-left: 10px;">A lightweight Dataset Explorer streamlit app that help to analyse different types dataset</span></div>',unsafe_allow_html=True,)
#----------------------------------------
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #F0F2F6;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: #333;
        z-index: 100;
    }
    .footer p {
        margin: 0;
    }
    .footer .highlight {
        font-weight: bold;
        color: blue;
    }
    </style>

    <div class="footer">
        <p>© 2025 | Created by : <span class="highlight">Avijit Chakraborty</span> | <a href="mailto:avijit.mba18@gmail.com"> 📩 </a></p> <span class="highlight">Thank you for visiting the app | Unauthorized uses or copying is strictly prohibited | For best view of the app, please zoom out the browser to 75%.</span>
    </div>
    """,
    unsafe_allow_html=True)

#---------------------------------------------------------------------------------------------------------------------------------
### Functions & Definitions
#---------------------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------------------
### Main App
#---------------------------------------------------------------------------------------------------------------------------------
col1, col2= st.columns((0.15,0.85))
with col1:           
    with st.container(border=True):
        
        st.info("""Upload your dataset **(CSV, XLS, XLSX, TXT, Parquet)** and explore the data.""")
        uploaded_file = st.file_uploader("📁 **:blue[Choose file]**",type=["csv", "xlsx", "xls", "txt", "parquet"])
        
        with col2:           

            if uploaded_file is not None:
                
                try:
                    if uploaded_file.name.endswith(".csv"):
                        df = pd.read_csv(uploaded_file)
                    elif uploaded_file.name.endswith(".parquet"):
                        df = pd.read_parquet(uploaded_file)
                    elif uploaded_file.name.endswith(".txt"):
                        df = pd.read_csv(uploaded_file, delimiter="\t")  # assuming tab-separated
                    elif uploaded_file.name.endswith((".xls", ".xlsx")):
                        df = pd.read_excel(uploaded_file)
                    else:
                        st.error("Unsupported file format.")
                        st.stop()

                    with st.container(border=True):
                        st.dataframe(df.head())

                    with st.container(border=True):
                        st.markdown("##### 📋 Data Overview")
                        
                        st.write(f"{df.shape[0]} rows × {df.shape[1]} columns")
                        dtype_df = df.dtypes.reset_index()
                        dtype_df.columns = ['Column', 'Data Type']
                        dtype_df['Data Type'] = dtype_df['Data Type'].astype(str)  # Convert to string for display
                        st.dataframe(dtype_df, use_container_width=True)

                    with st.container(border=True):
                        st.markdown("##### 📊 Descriptive Statistics")
                        numeric_df = df.select_dtypes(include='number')
                        if not numeric_df.empty:
                            st.write(numeric_df.describe())
                        else:
                            st.write("No numeric columns to describe.")

                    with st.container(border=True):
                        st.markdown("##### 🎨 Visualizations")
                        
                        subcol1, subcol2 = st.columns((0.15,0.85))
                        with subcol1:
                            viz_type = st.selectbox("**Choose a visualization**",["Histogram", "Correlation Heatmap", "Scatter Plot", "Bar Chart"])

                        with subcol2:
                            if viz_type == "Histogram":
                                col = st.selectbox("**Select column for histogram**", numeric_df.columns)
                                if col:
                                    fig, ax = plt.subplots(figsize=(15,5))
                                    numeric_df[col].hist(bins=20, ax=ax)
                                    ax.set_title(f'Histogram of {col}')
                                    ax.set_xlabel(col)
                                    ax.set_ylabel('Frequency')
                                    st.pyplot(fig,use_container_width=True)

                            elif viz_type == "Correlation Heatmap":
                                if numeric_df.shape[1] > 1:
                                    fig, ax = plt.subplots(figsize=(15,10))
                                    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)
                                    ax.set_title("Correlation Heatmap")
                                    st.pyplot(fig,use_container_width=True)
                                else:
                                    st.warning("Need at least 2 numeric columns for correlation.")

                            elif viz_type == "Scatter Plot":
                                if numeric_df.shape[1] >= 2:
                                    col1 = st.selectbox("**X-axis**", numeric_df.columns)
                                    col2 = st.selectbox("**Y-axis**", numeric_df.columns, index=1)
                                    fig, ax = plt.subplots(figsize=(15,5))
                                    ax.scatter(df[col1], df[col2], alpha=0.7)
                                    ax.set_xlabel(col1)
                                    ax.set_ylabel(col2)
                                    ax.set_title(f"Scatter Plot: {col1} vs {col2}")
                                    st.pyplot(fig,use_container_width=True)
                                else:
                                    st.warning("Need at least 2 numeric columns for scatter plot.")

                            elif viz_type == "Bar Chart":
                                cat_cols = df.select_dtypes(include='object').columns
                                if len(cat_cols) > 0:
                                    col = st.selectbox("**Select categorical column**", cat_cols)
                                    value_counts = df[col].value_counts()
                                    fig, ax = plt.subplots(figsize=(15,5))
                                    value_counts.plot(kind='bar', ax=ax)
                                    ax.set_title(f'Bar Chart of {col}')
                                    ax.set_xlabel(col)
                                    ax.set_ylabel('Count')
                                    plt.xticks(rotation=45)
                                    st.pyplot(fig,use_container_width=True)
                                else:
                                    st.warning("No categorical columns found.")

                except Exception as e:
                            st.error(f"Error processing file: {e}")
            else:
                st.warning("Please upload a file to get started.")