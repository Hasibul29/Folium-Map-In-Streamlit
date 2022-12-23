import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import jinja2
# from geopy.geocoders import Nominatim
import sqlite3
import datetime
import mysql
import mysql.connector as mysql
from db_connection import get_database_connection

hide_extra="""
<style>
#MainMenu{
  visibility: hidden;
}
footer{
 visibility: hidden;
}
Button{
 visibility: hidden;
}

</style>
"""

cursor,db = get_database_connection()


cursor.execute("Select * from mytable")
 
database = cursor.fetchall()

def mapval(str,strtdate,enddate):
    if str=='All':
        q = pd.read_sql_query(f"Select * from mytable where project_start_time > '{strtdate}' or project_completion_time < '{enddate}'",db)
    elif str=='Education':
        q = pd.read_sql_query("Select * from mytable where category='Education' and (project_start_time > '{strtdate}' or project_completion_time < '{enddate}') ",db)
    elif str=='Health':
        q = pd.read_sql_query("Select * from mytable where category='Health' and (project_start_time > '{strtdate}' or project_completion_time < '{enddate}') ",db)
    elif str=='Governance':
        q = pd.read_sql_query("Select * from mytable where category='Governance' and (project_start_time > '{strtdate}' or project_completion_time < '{enddate}') ",db)
    elif str=='Energy & Mining':
        q = pd.read_sql_query("Select * from mytable where category='Energy & Mining' and (project_start_time > '{strtdate}' or project_completion_time < '{enddate}') ",db)
    
    df = pd.DataFrame(q,columns=['project_name','category','affiliated_agency','description','project_start_time','project_completion_time','total_budget','completion_percentage','location_coordinates','comment'])

    # with open(r'./projects.csv',"r")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            as f:
    #     df = df.append(pd.read_csv(f),ignore_index=True)
    #     df = df.dropna()

    m = folium.Map(location=[23.73140275,90.39176192915883],zoom_start=12)

    folium.Marker(location=[23.73140275,90.39176192915883],popup='Your Location',tooltip='You').add_to(m)
    tooltip = "Click!"


    for (ind,row) in df.iterrows():
        template = jinja2.Template(open("PopUp.html").read())
        html = template.render(data=row[:-1],dataf=df)
        iframe = folium.IFrame(html,
                        width=450,
                        height=450 
                        )
        fpop = folium.Popup(iframe)

        l = row.loc['location_coordinates']
        l = l[1:-2]
        li = l.split(',')
        folium.Marker(
            li, popup=fpop, tooltip=tooltip
        ).add_to(m)

    folium_static(m)

def main():
    st.title('CodeSamurai')
    st.subheader('Project Map')
    st.markdown(hide_extra, unsafe_allow_html=True)
    # st.subheader('International Islamic University Chittagong')
    # # st.error('Updated version Coming Soon!!!')
    # st.sidebar.write('Menu')
    selected=st.sidebar.selectbox('Category',
                        ('All',
                        'Education',
                        'Health',
                        'Governance',
                        'Energy & Mining',
                        ))
    # col1,col2=st.columns((2,2))
    strtdate = st.sidebar.date_input(label='Start Date')
    enddate = st.sidebar.date_input(label='End Date')
    print(strtdate,enddate)
    if selected=='All':
        mapval('All',strtdate,enddate)
    elif selected=='Education':
        mapval('Education',strtdate,enddate)
    elif selected=='Health':
        mapval('Health',strtdate,enddate)
    elif selected=='Governance':
        mapval('Governance',strtdate,enddate)
    elif selected=='Energy & Mining':
        mapval('Energy & Mining',strtdate,enddate)

if __name__=='__main__':
    main()
