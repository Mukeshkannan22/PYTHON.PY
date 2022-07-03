import streamlit as st 
import time
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
col1,col2= st.columns(2)
with col1:
    st.image('https://media-exp1.licdn.com/dms/image/C560BAQE6FPEz390mzA/company-logo_200_200/0/1645521378225?e=2147483647&v=beta&t=0Fco09XDTCU3sEQdH03z7iiK4xLQO-Ybm8Vmyn1tbEY',width=100,caption='Know Your Story')
with col2:
    st.write('')
st.image('https://www.usda.gov/sites/default/files/covid-header-2.png')
st.title("COVID-19 ANALYSE")
st.write('A COVIDSafe Plan is a list of health and safety actions. It is an important part of the occupational health and safety obligations of every workplace and is required under the Victorian Government’s pandemic orders.Every Victorian business or organisation with on-site operations must keep a COVIDSafe Plan at each workplace. They must provide it to an Authorised Officer upon request and comply with any direction given by an authorised officer or WorkSafe inspector to modify the COVIDSafe plan. The plan must set out how the workplace will keep workers, customers and other attendees safe from COVID-19. It also helps to prepare for a case of COVID-19 in the workplace.All workplaces should regularly review and update their COVIDSafe Plan to ensure it reflects the current COVIDSafe settings. A COVIDSafe Plan template has been developed to assist workplaces. However, it is not mandatory to use this template.')

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
                st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTsvyCaSItjzfs38GnlEjEiuNgEW0bNQOi3KA&usqp=CAU'width=500)
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
                total_deaths=list(new_2['RUNNING_TOTAL'])
                today_2 = datetime.date.today()
                
                curr_time = time.strftime("%H:%M:%S", time.localtime())
 
                st.write(f'In {selectedCountry2}, from {today_2} to {curr_time} CEST,cases of COVID-19 with {total_deaths[-1]} deaths, reported to WHO.')
                st.plotly_chart(runn)
            if page_value == 'Recovery':
                st.error('🔜 Recovery page is Work in Progress 🚧 ')  
        else:
            st.warning('Incorrct Password')
                
elif choice == 'SIGN-UP':
    st.subheader('CREATE NEW ACCOUNT')
    new_user = st.text_input('User Name ')
    new_password= st.text_input('Enter Password',type='password')
    dob=st.date_input('Date of Birth')
    check=st.checkbox('T&C Apply')
    if st.button('Sign-up'):
        if check:
            def user(new_password):
                sp="$#@"
                ret=True
                if not any(i in sp for i in new_password):
                    st.warning("At least 1 character form[$#@]")
                    ret=False
                if not any(i.isupper() for i in new_password ):
                    st.warning("At least 1 letter between[A-Z]")
                    ret=False
                if not any(i.islower() for i in new_password):
                    st.warning("At least 1 letter between[a-z]")
                    ret=False
                if not any(i.isdigit() for i in new_password):
                    st.warning("At least 1 number between [0-9]")
                    ret=False
                if len(new_password)<6:
                    st.warning("Minimum length of transaction password :6")
                    ret=False
                if len(new_password)>12:
                    st.warning("Maximum length of transaction password :12")
                    ret=False
                if ret:
                    return ret
        else:
            st.warning('Click The Check Box')        
                
        if user(new_password):
            create_table()
            user_data(new_user,new_password)
            st.success('You Have a successfully created  avalidd Account')
            st.info("Go to Log in Menu to Login")
            st.balloons()
    
