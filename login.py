from tabnanny import check
import streamlit as st 
import time
import pandas as pd 
import plotly.express as px
import sqlite3 
connect=sqlite3.connect('data.db')
c=connect.cursor()
import datetime
import streamlit.components.v1 as components

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
st.set_page_config(layout="wide")
new_df = confrimed_df.melt(id_vars=['Country/Region','Province/State','Lat','Long'])
col1,col2= st.columns(2)

#with col1:
#   st.image('https://www.imperial.ac.uk/ImageCropToolT4/imageTool/uploaded-images/newseventsimage_1585324917059_mainnews2012_x1.jpg',width=150,caption='')
#with col2:
#    st.write('')

st.image('https://www.usda.gov/sites/default/files/covid-header-2.png')
st.title("COVID-19 ANALYSE")
st.write('A COVIDSafe Plan is a list of health and safety actions. It is an important part of the occupational health and safety obligations of every workplace and is required under the Victorian Government’s pandemic orders.Every Victorian business or organisation with on-site operations must keep a COVIDSafe Plan at each workplace. They must provide it to an Authorised Officer upon request and comply with any direction given by an authorised officer or WorkSafe inspector to modify the COVIDSafe plan. The plan must set out how the workplace will keep workers, customers and other attendees safe from COVID-19. It also helps to prepare for a case of COVID-19 in the workplace.All workplaces should regularly review and update their COVIDSafe Plan to ensure it reflects the current COVIDSafe settings. A COVIDSafe Plan template has been developed to assist workplaces. However, it is not mandatory to use this template.')
components.html(
    """
     <div class='tableauPlaceholder' id='viz1656936464205' style='position: relative'><noscript><a href='#'>
<img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;co&#47;covid19_16386879014100&#47;Dashboard1&#47;1_rss.png' style='border: none' />
</a>
</noscript>
<object class='tableauViz'  style='display:none;'>
<param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> 
<param name='embed_code_version' value='3' /> 
<param name='site_root' value='' />
<param name='name' value='covid19_16386879014100&#47;Dashboard1' />
<param name='tabs' value='yes' /><param name='toolbar' value='yes' />
<param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;co&#47;covid19_16386879014100&#47;Dashboard1&#47;1.png' /> 
<param name='animate_transition' value='yes' />
<param name='display_static_image' value='yes' />
<param name='display_spinner' value='yes' />
<param name='display_overlay' value='yes' />
<param name='display_count' value='yes' />
<param name='language' value='en-US' />
</object></div>                
<script type='text/javascript'>                    
var divElement = document.getElementById('viz1656936464205');                    
var vizElement = divElement.getElementsByTagName('object')[0];                    
if ( divElement.offsetWidth > 800 ) { vizElement.style.minWidth='820px';vizElement.style.maxWidth='100%';vizElement.style.minHeight='810px';vizElement.style.maxHeight=(divElement.offsetWidth*0.75)+'px';} 
else if ( divElement.offsetWidth > 500 ) { vizElement.style.minWidth='1220px';vizElement.style.maxWidth='100%';vizElement.style.minHeight='810px';
vizElement.style.maxHeight=(divElement.offsetWidth*0.75)+'px';} 
else { vizElement.style.width='100%';vizElement.style.minHeight='800px';vizElement.style.maxHeight=(divElement.offsetWidth*1.77)+'px';}                     var scriptElement = document.createElement('script');        
scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
vizElement.parentNode.insertBefore(scriptElement, vizElement);               
</script>
    """,
    height=1000, width=1200
)

menu=['TABLEAU PERVIVEW YEARS REPORT','LOGIN','SIGN-UP']
choice=st.sidebar.selectbox('MENU',menu)
if choice == 'HOME':
    st.subheader('HOME')
elif choice=='LOGIN':
    st.sidebar.subheader('LOGIN')
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
                st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTsvyCaSItjzfs38GnlEjEiuNgEW0bNQOi3KA&usqp=CAU',width=500)
                country_list = list(new_df['Country/Region'].unique())
                selectedCountry  = st.sidebar.selectbox('Select Country', country_list)

                new_df['Daily_Case'] = new_df[new_df['Country/Region'] == selectedCountry]['value'].apply(lambda x: int(dailyCaseClac(x)))

                new_df['Daily_Case'] = new_df['Daily_Case'].fillna(0).astype(int)
                df_selectedCountry = new_df[new_df['Country/Region'] == selectedCountry]
                fig = px.area(df_selectedCountry,x = 'variable',y = 'Daily_Case',)
                fig.update_traces(line_color='#39bbf7')
                fig.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))
                fig.update_layout({'plot_bgcolor':'rgba(0,0,0,0)','paper_bgcolor':'rgba(0,0,0,0)'})
                today = datetime.date.today()
                st.title(today)
                today_case=list(df_selectedCountry['Daily_Case'])
                st.header(f'Coronavirus LIVE Updates: {selectedCountry} Records {today_case[-1]} New COVID-19 Cases In Last 24 Hours')
                st.plotly_chart(fig)
                st.table(df_selectedCountry.tail(5))
            if page_value == 'Deaths':
                st.image('data:image/jpeg;base64,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',caption='“The end is nightWe are sure to dieBut we still have to try”― Dylan Lehman')
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
    new_user = st.sidebar.text_input('User Name ')
    new_password= st.sidebar.text_input('Enter Password',type='password')
    dob=st.sidebar.date_input('Date of Birth')
    check=st.sidebar.checkbox('T&C Apply')
    if st.sidebar.button('Sign-up'):
        if check:
            def user(new_password):
                sp="$#@"
                ret=True
                if not any(i in sp for i in new_password):
                    st.sidebar.warning("At least 1 character form[$#@]")
                    ret=False
                if not any(i.isupper() for i in new_password ):
                    st.sidebar.warning("At least 1 letter between[A-Z]")
                    ret=False
                if not any(i.islower() for i in new_password):
                    st.sidebar.warning("At least 1 letter between[a-z]")
                    ret=False
                if not any(i.isdigit() for i in new_password):
                    st.sidebar.warning("At least 1 number between [0-9]")
                    ret=False
                if len(new_password)<6:
                    st.sidebar.warning("Minimum length of transaction password :6")
                    ret=False
                if len(new_password)>12:
                    st.sidebar.warning("Maximum length of transaction password :12")
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
    
