import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# st.title("Explanatory Data Analysis")
# st.sidebar.title("Upload Data")
st.set_page_config(layout="wide")

col1,col2,col3 = st.columns([10,5,50])
with col1:
        st.image("fresh_TIH_logo.jpeg")
with col3:
        st.title("XInsights")
        st.header("Explainable Visuals")
col4=st.columns(7)

col5,col6,col7= st.columns([10,5,50])
with col5:
    uploaded_data=st.file_uploader("Upload csv file",type = ['csv','xlsx']) 
with col7:
    tab1,tab2,tab3,tab4=st.tabs(['Data Info','Numeric Features','Categorical Features','Show Data'])
    def check1(data):
        if uploaded_data is not None:
            if uploaded_data.type=='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                data1=pd.read_excel(uploaded_data)
                data1.to_csv("test.csv") 
                val = pd.DataFrame(pd.read_csv("test.csv"))
                return(val) 
            else:
                val=pd.read_csv(uploaded_data) 
                return(val)
        return(val)     
    if uploaded_data is not None:
            # print(uploaded_data.type)
            # data = pd.read_csv(uploaded_data)
            data=check1(uploaded_data)
            with tab1:
                rows=data.shape[0]
                cols= data.shape[1]
                duplicates=data[data.duplicated()]
                no_duplicates= duplicates.shape[0]
                no_missing_val= data[data.isna().any(axis=1)].shape[0]
                st.title("Meta Data")
                table_markdown= f"""
                    | Description| Value|
                    |-------------|------|
                    | Number of Rows | {rows}|
                    | Number of Columns | {cols}
                    | Number of Duplicate Rows | { no_duplicates}|
                    | Number of missing values | {no_missing_val}|
                    """
                st.markdown(table_markdown)
                st.title("Column Information")
                columns = list(data.columns)
                table_2 = pd.DataFrame({"Columns":columns,"Types": data.dtypes.to_list()})
                st.dataframe(table_2,hide_index=True)    
            with tab2:
                st.header("Numeric Features to be explored")
                num_col= data.select_dtypes(include="number").columns.to_list()
                selected_col=st.selectbox("What column do you want to choose?",num_col)
                st.header(f"{selected_col} - Statistics")
                col1= data[selected_col].nunique()
                col2= data[selected_col].isna().sum()
                col3=data[selected_col].eq(0).sum()
                col4=data[selected_col].lt(0).sum()
                col5= data[selected_col].mean()
                col6=data[selected_col].median()
                col7=np.sqrt(data[selected_col].var())
                col8=data[selected_col].min()
                col9=data[selected_col].max()
                dict={"No.of Unique Values":col1,"No.of Rows with Missing Values": col2,"No.of Rows with 0": col3,"No.of Rows with negative Values": col4,"Average Value": col5,"Median": col6,"Min Value": col8,"Max Value": col9,"Sd":col7}
                info_df=pd.DataFrame(list(dict.items()),columns=["description","Value"])
                st.dataframe(info_df)
                st.header("Histogram")
                plt.hist(data[selected_col])
                st.pyplot()  
            with tab3:
                st.header("Categorical Features Exploring")  
                cat_fea=data.select_dtypes(include='object').columns.to_list()
                selected_cat=st.selectbox("Choose a categorical feature",cat_fea)
                cat_col={}
                cat_col["No.of unique values"]=data[selected_cat].nunique()
                cat_col["No.of Rows with missing values"]= data[selected_cat].isna().sum()
                cat_col["No.of Empty Rows"]=data[selected_cat].eq("").sum()
                cat_col["No. of Rows with only whitespaces"]=data[selected_cat].str.isspace().sum()
                cat_col["No.of rows with uppercases"]=data[selected_cat].str.isupper().sum()
                cat_col["No. of Rows with Alphabets"]=data[selected_cat].str.isalpha().sum()
                cat_col["No.of Rows with only digits"]=data[selected_cat].str.isdigit().sum()
                cat_df=pd.DataFrame(list(cat_col.items()),columns=["Description","Values"])
                st.table(cat_df)
            with tab4:
                st.header("Data is as follows:")
                st.dataframe(data)
        