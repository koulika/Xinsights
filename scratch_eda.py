import streamlit as st
# import duckdb
import re
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import f_oneway,chi2_contingency,kruskal,kstest,probplot,kurtosis,skew
import plotly.figure_factory as ff
# from chart_spec_bar1 import *
# from chart_spec5 import *
# import warnings
# warnings.filterwarnings("ignore")
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
    tab0,tab1,tab2,tab3,tab4,tab5,tab6,tab7=st.tabs(["Dimension and Measures",'Data Info','Numeric Features','Categorical Features','Show Data and Its Distribution','Bivariate-Correlation','Multivariate-Correlation','Outliers'])
    def check1(data):
        if uploaded_data is not None:
            if uploaded_data.type=='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                data1=pd.read_excel(uploaded_data)
                data1.to_csv("test.csv") 
                val = pd.DataFrame(pd.read_csv("test.csv"))
                # val=duckdb.sql("From sniff_csv('test.csv')")
                return(val) 
            else:
                val=pd.read_csv(uploaded_data) 
                # val=duckdb.sql("From sniff_csv('test.csv')")
                return(val)
        return(val)     
    if uploaded_data is not None:
            # print(uploaded_data.type)
            # data = pd.read_csv(uploaded_data)
            data=check1(uploaded_data)
            # with tab0:
            #     df=duckdb.sql("Select * from data").fetchall()
            #  st.table(df)
                # con= duckdb.connect()
                # con.execute("CREATE TABLE my_table AS SELECT * FROM data")
                # duckdb.sql("INSERT INTO my_table BY NAME SELECT * FROM data")
                # con.execute("INSERT INTO test_df_table SELECT * FROM data")
            with tab0:
                #  tab_dim,tab_mea=st.tabs(["Dimension","Measures"])
                #  with tab_dim:
                #     st.title("Dimension")
                    cat_bool_col= data.select_dtypes(include=['object','bool']).columns.to_list()
                #     data_1=pd.DataFrame(cat_col)
                #     st.data_editor(data_1, num_rows="dynamic")
                #  with tab_mea:  
                #     st.title("Measures")
                    num_col=data.select_dtypes(include='number').columns.to_list()
                #     data_2=pd.DataFrame(num_col)
                #     st.data_editor(data_2,num_rows="dynamic")
                    dim_mea=[]
                    for i in data.columns:
                        if(i in cat_bool_col):
                            dim_mea.append('Dimension')
                        else:
                            dim_mea.append('Measure')    
                    dict_dim_mea={"Column Name": data.columns,'Dimeansion/Measure':dim_mea}
                    st.table(dict_dim_mea)
            with tab1:
                rows=data.shape[0]
                cols= data.shape[1]
                duplicates=data[data.duplicated()]
                no_duplicates= duplicates.shape[0]
                no_missing_val= data[data.isna().any(axis=1)].shape[0]
                st.title("Meta Data")
                # table_markdown= f"""
                #     | Description| Value|
                #     |-------------|------|
                #     | Number of Rows | {rows}|
                #     | Number of Columns | {cols}
                #     | Number of Duplicate Rows | { no_duplicates}|
                #     | Number of missing values | {no_missing_val}|
                #     """
                # st.markdown(table_markdown)
                dict1={"Description":['Number of Rows','Number of Columns','Number of Duplicate Rows','Number of missing values'],"Values":[rows,cols,no_duplicates,no_missing_val]}
                df= pd.DataFrame(dict1)
                st.table(df)
                st.title("Column Wise Information")
                cat_col= data.select_dtypes(include='object').columns.to_list()
                for j in cat_col:
                    flag=0
                    c=[]
                    for i in data[j]:
                        test_str = i
                        pattern_str_1 = r'^\d{4}-\d{2}-\d{2}$'
                        pattern_str_2= r'^\d{2}-\d{2}-\d{4}$'
                        if re.match(pattern_str_1, str(test_str)) or re.match(pattern_str_2, str(test_str)):
                            # print("True")
                            c.append('True')
                        else:
                            # print("False")
                            c.append('False')
                    # print(type(c))
                    for z in c:
                        if(z=='True'):
                            flag=flag+1
                        else:
                            flag= flag-1  
                    if(flag>=1):
                        data[j]=data[j].astype('datetime64[ns]')
                # dictionary={'datatypes':data.dtypes} 
                # show=pd.DataFrame(dictionary)   
                # st.dataframe(show)         
                datatype=[]
                uni=[]
                miss=[]
                zer=[]
                inf=[]
                for i in data.columns:
                    miss.append(data[i].isna().sum())
                    uni.append((data[i].nunique()))
                    inf.append(data[i].isin([np.inf, -np.inf]).sum())
                    if(data.dtypes[i]=="int64"):
                        datatype.append('Numerical (Integer)')
                        zer.append(data[i][data[i]==0].count())
                    elif(data.dtypes[i]=='float'):
                        datatype.append('Numerical (Decimal Point)')
                        zer.append(data[i][data[i]==0].count())
                    elif(data.dtypes[i]=='object'):
                        datatype.append('Categorical')
                        zer.append(0)
                    elif(data.dtypes[i]=='bool'):
                        datatype.append('Boolean')
                        zer.append(0) 
                    else:
                         datatype.append('Date')
                         zer.append(0)       
                st.table({"Column Name":data.columns,"Column Type":datatype,"No. of Unique Values":uni,"No. of Missing Values":miss,"Count of Zero Values":zer,"Count of Infinity":inf})
                # st.title("No of Unique Values in each Column")
                # data_num_uni=pd.DataFrame( [(i, data[i].nunique()) for i in data.columns], columns=["Column Name","No. of Unique Values"])
                # st.dataframe(data_num_uni)   
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
                col10= skew(data[selected_col],axis=0)
                col11=kurtosis(data[selected_col],axis=0)
                col12=data[selected_col].quantile(0.25)
                col13=data[selected_col].quantile(0.75)
                dict={"No.of Unique Values":col1,"No.of Rows with Missing Values": col2,"No.of Rows with 0": col3,"No.of Rows with negative Values": col4,"Average Value": col5,"Median": col6,"Min Value": col8,"Max Value": col9,"Sd":col7,"Skewness":col10,"Kurtosis":col11,"25th Quantile":col12,"75 th Quantile":col13}
                info_df=pd.DataFrame(list(dict.items()),columns=["description","Value"])
                st.dataframe(info_df)
                # skewness= data[num_col].skew()
                # st.write(skewness)
                st.header("Histogram")
                # histogram1= px.histogram(data[selected_col],nbins=50,histnorm='probability density')
                # histogram1.add_vline(x=np.mean(data[selected_col]), line_dash = 'dash', line_color = 'firebrick')
                # dictionary_1= {"tick0":0,"dtick" :500}
                # histogram1=go.Figure(data=[go.Histogram(x=data[selected_col])])
                # histogram1.update_layout(bargap=0.2,xaxis_title=selected_col,yaxis_title="Proportion")
                # st.plotly_chart(histogram1) 
                hist=[data[selected_col]]
                group=['Distplot']
                figure= ff.create_distplot(hist,bin_size=0.5,group_labels=group,show_hist=True,show_rug=False) 
                figure.add_vline(np.mean(data[selected_col]),line_dash='dash',line_color = 'firebrick')
                figure.update_layout(bargap=0.2,xaxis_title=selected_col,yaxis_title="Proportion")
                st.plotly_chart(figure) 
                # chart_spec_hist=generate_chart_specs(data,selected_col, x_encoding_type="quantitative", mark_type="bar")
                # st.vega_lite_chart(chart_spec_hist)
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
                st.header("Unique Categories in the selected Column")
                df=pd.DataFrame(list(data[selected_cat].unique()),columns=["Unique Categories"])
                st.table(df)
                hist_cat=px.histogram(data[selected_cat])
                hist_cat.update_layout(bargap=0.2,xaxis_title="Column_Values",yaxis_title="Frequency")
                st.plotly_chart(hist_cat)
            with tab4:
                st.header("Data is as follows:")
                st.dataframe(data)
                num_col=data.select_dtypes(include=['number']).columns.to_list()
                x=st.selectbox("Select a column to check its Distribution",num_col)
                test_stat= kstest(data[x],"norm",alternative='two-sided')
                print(test_stat)
                st.write("p value is:",test_stat[1])
                if(round(test_stat[1],3)<=0.05):
                    st.write("Datapoints are not Normally Distributed")
                else:
                    st.write("Datapoints are Normally Distributed")
                qq= probplot(data[x],dist='norm',plot=plt)
                st.pyplot(plt.gcf())
            with tab5:
                #  column1,column2,column3= st.columns([2,1,2])
                #  column4,column5,column6= st.columns([2,1,2])
                #  num_col= data.select_dtypes(include="number").columns.to_list()
                #  with column1:
                    col_except_date= data.select_dtypes(exclude=['datetime','bool']).columns.to_list()
                    x=st.selectbox("Select first column",col_except_date)
                    with st.expander("See the type"):
                        if(data.dtypes[x]=='int64'):
                            st.write("Numerical Integer") 
                        elif(data.dtypes[x]=='float'):
                            st.write("Numerical Decimal Point")
                        elif(data.dtypes[x]=='object'):
                             st.write("Categorical")      
                # with column4: 
                    y=st.selectbox("Select Second column",col_except_date)
                    with st.expander("See the type"):
                        if(data.dtypes[y]=='int64'):
                            st.write("Numerical Integer") 
                        elif(data.dtypes[y]=='float'):
                            st.write("Numerical Decimal Point")
                        elif(data.dtypes[y]=='object'):
                             st.write("Categorical")                
                    if (st.button("Show the Correlation")==True):
                        if((data.dtypes[x]=='float' or data.dtypes[x]=='int64') and (data.dtypes[y]=='float' or data.dtypes[y]=='int64') ):
                            # z=st.selectbox("Choose the type of correlation",['Pearson','Kendall','Spearman'])
                            correlation_P = data[x].corr(data[y])
                            st.write("The Pearson's correlation between x and y is",round(correlation_P,3))
                            correlation_K = data[x].corr(data[y],method='kendall')
                            st.write("The Kendall's correlation between x and y is",round(correlation_K,3))
                            correlation_S = data[x].corr(data[y],method='spearman')
                            st.write("The Spearman's correlation between x and y is",round(correlation_S,3))
                            if (round(correlation_K,3)> 0.500):
                                 st.write("Two columns are positively associated or correlated")
                            else:
                                 st.write("Two columns are negatively associated or correlated")     
                            fig, ax = plt.subplots()
                            ax.scatter(data[x],data[y])
                            st.pyplot(fig,use_container_width=True)
                            # chart_spec_scatter=generate_chart_specs(data,x,y,x_encoding_type = "quantitative", y_encoding_type="quantitative", mark_type="point")
                            # st.vega_lite_chart(chart_spec_scatter)      
                        # categorical vs numeric
                        if (data.dtypes[x]=='object' and data.dtypes[y]=='float'):
                            cat_col= data.groupby(data[x])[y].apply(list)
                            # result_1= f_oneway(*cat_col)
                            resultk_1=kruskal(*cat_col,nan_policy='omit')
                            #   st.write(results)
                            # st.write("pvalue is for Annova test: ",round(result_1[1],4))
                            st.write("pvalue is for Kruskal Wallis test: ",round(resultk_1[1],4))
                            if(round(resultk_1[1],4)<0.05):
                                  st.write("Two columns are associated or correlated")
                            else:
                                  st.write("Two columns are not associated or correlated")
                            fig= px.box(data,x=x,y=y)
                            st.plotly_chart(fig)  
                            # chart_spec_box=generate_chart_specs(data,x,y, x_encoding_type="nominal", y_encoding_type="quantitative",mark_type="boxplot")
                            # st.vega_lite_chart(chart_spec_box) 
                        elif(data.dtypes[x]=='float' and data.dtypes[y]=='object'):
                             cat_col= data.groupby(data[y])[x].apply(list)
                            #  result_2= f_oneway(*cat_col)
                             resultk_2=kruskal(*cat_col,nan_policy='omit')
                            #  st.write("pvalue is: ",round(result_2[1],4)) 
                             st.write("pvalue is for Kruskal Wallis test: ",round(resultk_2[1],4))
                             if(round(resultk_2[1],4)<0.05):
                                  st.write("Two columns are associated or correlated")
                             else:
                                  st.write("Two columns are not associated or correlated")
                             fig =px.box(data,x=y,y=x)
                             st.plotly_chart(fig)
                            #  chart_spec_box=generate_chart_specs(data,y,x, x_encoding_type="nominal", y_encoding_type="quantitative",mark_type="boxplot")
                            #  st.vega_lite_chart(chart_spec_box) 
                        # categorical vs categorical
                        if(data.dtypes[x]=='object' and data.dtypes[y]=='object'):
                             chisqr= pd.crosstab(data[x],data[y],margins=True)
                             stat,p,df= chi2_contingency(chisqr)[0:3] 
                             st.write("P-value is :",p)
                             if(p<=0.05):
                                  st.write("Two columns are associated or correlated")
                             else:
                                  st.write("Two columns are not associated or correlated")             
            with tab6:
                 mul_corr_p= data.corr(numeric_only=True)
                 st.write("Pearson's Correlation Coefficients")
                 heatmap_p = px.imshow(mul_corr_p,text_auto=True) 
                 st.plotly_chart(heatmap_p)
                 st.write("Kendall's Correlation Coefficients")
                 mul_corr_k= data.corr(method='kendall',numeric_only=True)
                 heatmap_k= px.imshow(mul_corr_k,text_auto=True) 
                 st.plotly_chart(heatmap_k)
                 st.write("Spearman's Correlation Coefficients")
                 mul_corr_s= data.corr(method='spearman',numeric_only=True)
                 heatmap_s= px.imshow(mul_corr_s,text_auto=True) 
                 st.plotly_chart(heatmap_s) 
            with tab7:
                    outlier=[]
                    c=0
                    d={}
                    for i in num_col:
                         c=0
                #    Z-score method of detecting outliers
                        #  miu= np.mean(data[i])
                        #  sd=np.std(data[i])
                        # #  st.write("mean is:",miu,"sd is :",sd)
                        #  for j in data[i]:
                        #       z= (j-miu)/sd
                        #       if(z>3 or z<-3):
                        #            c=c+1
                                #    outlier= outlier.append(j)
                    #     #  st.write("Number of Outliers of column",i,"is : ",c)
                        #  d[i]=c 
                    #      out_df=pd.DataFrame(list(d.items()),columns=["Column_Name","No.of Outliers"]) 
                    # st.table(out_df)            
                         q1= data[i].quantile(0.25)
                         q3= data[i].quantile(0.75)
                         IQR= q3-q1
                         ub= q3+1.5*IQR
                         lb= q1-1.5*IQR
                         for j in data[i]:
                            if(j<lb or j>ub):
                                    # outlier.append(j)
                                    c=c+1
                         d[i]=c
                        #  d["outlier is"]=outlier
                         out_df=pd.DataFrame(list(d.items()),columns=["Column_Name","No.of Outliers"]) 
                    st.table(out_df) 
                    fig1= px.box(data[num_col]) 
                    fig1.update_layout(
                                    title= "BOXPLOT OF NUMERIC COLUMNS",
                                    xaxis_title="Variables",
                                    yaxis_title="Values"  
                                    )           
                    st.plotly_chart(fig1)



     
                      
     