import pandas as pd
import streamlit as st
import numpy as np

st.title('COVID-19')
df=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
new_df = df.melt(id_vars=['Country/Region','Province/State','Lat','Long'])
new=new_df[new_df['Country/Region']=='India'].sort_values(by=['value'])
a=[nn-n for n,nn in zip(new['value'],new['value'][1:]+[0])]
a.insert(0,0)
new['CUM- SUM']=a
s=st.dataframe(new)
print(s)
m=st.dataframe(a)
st.line_chart(m)
