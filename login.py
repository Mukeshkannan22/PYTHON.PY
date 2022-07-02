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
st.title('GWC - DASHBOARD')


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
                st.plotly_chart(fig)
                
                new=new_df[new_df['Country/Region']=='India'].sort_values(by=['value'])
                a=[nn-n for n,nn in zip(new['value'],new['value'][1:]+[0])]
                a.insert(0,0)
                new['Cum-sum']=a
                daily=pd.DataFrame(new[['value','Cum-sum']])
                fig2=px.pie(daily)
                st.plotly_chart(fig2)
                st.table(df_selectedCountry)
            if page_value == 'Cases':
                death_df=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
                death_pvt_df=df_d.melt(id_vars=['Province/State','Country/Region','Lat','Long'],var_name='Date',value_name='RUNNING_TOTAL')
                new_2=death_pvt_df[death_pvt_df['Country/Region']=='India'].sort_values(by=['RUNNING_TOTAL'])
                b=[nn-n for n,nn in zip(new_2['RUNNING_TOTAL'],new_2['RUNNING_TOTAL'][1:]+[0])]
                b.insert(0,0)
                new_2['Cum-sum']=b
                st.table(new_2.tail(1))
                l=new_2[new_2['Country/Region']=='India']
                cum=px.line(l['Cum-sum'])
                runn=px.line(l['RUNNING_TOTAL'])
                st.plotly_chart(cum)
                st.plotly_chart(runn)
        else:
            st.warning('Incorrct Password')
                
elif choice == 'SIGN-UP':
    st.subheader('CREATE NEW ACCOUNT')
    new_user = st.text_input('User Name ')
    new_password= st.text_input('Enter Password',type='password')
    
    if st.button('SIGN-IN'):
        create_table()
        user_data(new_user,new_password)
        st.success('You Have a successfully created  avalidd Account')
        st.info("Go to Log in Menu to Login")
        
