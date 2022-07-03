import streamlit as st 
import pandas as pd 
import plotly.express as px
import sqlite3 
connect=sqlite3.connect('data.db')
c=connect.cursor()
import datetime

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS user(username TEXT , password TEXT)')
def user_data(username,password):
    c.execute('INSERT INTO user(username, password) values(?,?)',(username,password))
    connect.commit()
def login(username,password):
    c.execute('SELECT * FROM user where username=? and password = ? ',(username,password))
    data=c.fetchall()
    return data 
confrimed_covid = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'

confrimed_df = pd.read_csv(confrimed_covid)

new_df = confrimed_df.melt(id_vars=['Country/Region','Province/State','Lat','Long'])
st.markdown('**GWC_DASHBOARDS**')
col1, col2, col3 = st.columns(3)
with col2:
    st.image("https://media-exp1.licdn.com/dms/image/C560BAQE6FPEz390mzA/company-logo_200_200/0/1645521378225?e=2147483647&v=beta&t=0Fco09XDTCU3sEQdH03z7iiK4xLQO-Ybm8Vmyn1tbEY",width=50,caption='Know Your Story')
with col3:
    st.markdown('**GWC_DASHBOARDS**')
st.title("COVID-19 ANALIYSE")

menu=['HOME','LOGIN','SIGN-UP']
choice=st.sidebar.selectbox('MENU',menu)
if choice == 'HOME':
    st.subheader('HOME')
elif choice=='LOGIN':
    st.subheader('LOGIN')
    username=st.sidebar.text_input('USER NAME')
    password=st.sidebar.text_input('PASSWORD',type='password')
    if st.sidebar.checkbox('LOGIN'):
        
        create_table()
        result= login(username,password)
        if result:
            st.snow()
            st.success(f'LOGGED IN AS {username}')
            temp_val = 0
            def dailyCaseClac(x):
                global temp_val
                currentVal = x - temp_val
                temp_val = x
                return int(currentVal)
            page_value  = st.sidebar.radio('Select Page', ['Cases','Deaths','Recovery'])
            print(page_value)
            if page_value == 'Cases':
                st.header('Covid Cases')

                country_list = list(new_df['Country/Region'].unique())
                selectedCountry  = st.sidebar.selectbox('Select Country', country_list)

                new_df['Daily_Case'] = new_df[new_df['Country/Region'] == selectedCountry]['value'].apply(lambda x: int(dailyCaseClac(x)))

                new_df['Daily_Case'] = new_df['Daily_Case'].fillna(0).astype(int)
                df_selectedCountry = new_df[new_df['Country/Region'] == selectedCountry]
                fig = px.line(df_selectedCountry,x = 'variable',y = 'Daily_Case',)
                today = datetime.date.today()
                st.title(today)
                today_case=list(df_selectedCountry['Daily_Case'])
                st.header(f'Coronavirus LIVE Updates: {selectedCountry} Records {today_case[-1]} New COVID-19 Cases In Last 24 Hours')
                st.plotly_chart(fig)
                st.table(df_selectedCountry.tail(5))
            if page_value == 'Deaths':
                country_list = list(new_df['Country/Region'].unique())
                selectedCountry2 = st.sidebar.selectbox('Select Country', country_list)
                death_df=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
                death_pvt_df=death_df.melt(id_vars=['Province/State','Country/Region','Lat','Long'],var_name='Date',value_name='RUNNING_TOTAL')
                new_2=death_pvt_df[death_pvt_df['Country/Region']==selectedCountry2]
                b=[nn-n for n,nn in zip(new_2['RUNNING_TOTAL'],new_2['RUNNING_TOTAL'][1:]+[0])]
                b.insert(0,0)
                new_2['Cum-sum']=b
                st.table(new_2.tail(1))
                l=new_2[new_2['Country/Region']==selectedCountry2]
                cum=px.line(l['Cum-sum'])
                runn=px.line(l['RUNNING_TOTAL'])
                today_deaths=list(new_2['Cum-sum'])
                st.header(f'Coronavirus LIVE Updates: {selectedCountry2} Records {today_deaths[-1]} New COVID-19 Cases In Last 24 Hours')
                st.plotly_chart(cum)
                st.plotly_chart(runn)
            #if page_value = 'Recovery':
             #   pass
                    
        else:
            st.warning('Incorrct Password')
                
elif choice == 'SIGN-UP':
    st.subheader('CREATE NEW ACCOUNT')
    new_user = st.text_input('User Name ')
    new_password= st.text_input('Enter Password',type='password')
    st.balloons()
    
    if st.button('SIGN-IN'):
        create_table()
        user_data(new_user,new_password)
        st.success('You Have a successfully created  avalidd Account')
        st.info("Go to Log in Menu to Login")
        
