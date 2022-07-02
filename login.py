from debugpy import connect
import streamlit as st 
import pandas as pd 
import plotly.express as px
import sqlite3 
connect=sqlite3.connect('data.gwc')
c=connect.cursor()

def create_table():
    c.execute('CREAT TABLE IF NOT EXISTS user(username TEXT , password TEXT)')


confrimed_covid = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'

confrimed_df = pd.read_csv(confrimed_covid)

new_df = confrimed_df.melt(id_vars=['Country/Region','Province/State','Lat','Long'])
st.title('GWC - DASHBOARD')


st.title("WLECOME")
menu=['HOME','LOGIN','SIGN-UP']
choice=st.sidebar.selectbox('MENU',menu)
if choice == 'HOME':
    st.subheader('HOME')
elif choice=='LOGIN':
    st.subheader('LOGIN')
    username=st.sidebar.text_input('USER NAME')
    password=st.sidebar.text_input('PASSWORD',type='password')
    if st.sidebar.button('LOGIN'):
        if password == '12345':
            st.success(f'LOGGED IN AS {username}')
            page_value  = st.sidebar.radio('Select Page', ['Demo', 'Cases'])
            print(page_value)
            temp_val = 0
            def dailyCaseClac(x):
                global temp_val
                currentVal = x - temp_val
                temp_val = x
                return int(currentVal)

            # This is the streamlit method explanation


            if page_value == 'Demo':

                st.write('Hello World ***Accepts Markdown as well***')
                st.text('Hello World from Streamlit.text')

                st.title("this is the Title Card")
                st.header('This is the header text')
                st.subheader('This is the sub title')
                st.dataframe(confrimed_df)
                st.table(confrimed_df[['Country/Region', 'Province/State']])



            if page_value == 'Cases':
                st.header('Covid Cases')

                country_list = list(new_df['Country/Region'].unique())
                selectedCountry  = st.sidebar.selectbox('Select Country', country_list)

                new_df['Daily_Case'] = new_df[new_df['Country/Region'] == selectedCountry]['value'].apply(lambda x: int(dailyCaseClac(x)))

                new_df['Daily_Case'] = new_df['Daily_Case'].fillna(0).astype(int)
                df_selectedCountry = new_df[new_df['Country/Region'] == selectedCountry]

                # st.dataframe(new_df[new_df['Country/Region'] == selectedCountry].tail())

                fig = px.line(df_selectedCountry,x = 'variable',y = 'Daily_Case',)

                st.plotly_chart(fig)
                
                st.table(df_selectedCountry)
            else:
                st.warning('Incorrct Password')
                
elif choice == 'SIGN-UP':
    st.subheader('CREATE NEW ACCOUNT')
    new_user = st.text_input('User Name ')
    new_password= st.text_input('Enter Password',type='password')
    
    if st.button('SIGN-IN'):
        st.success('You Have a successfully created  avalidd Account')
        st.info("Go to Log in Menu to Login")
        
               
