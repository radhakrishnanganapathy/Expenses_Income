import streamlit as st
from datetime import datetime
from DataBase import database
import pandas as pd
import plotly.express as px

cursor = database()
# end = datetime.end().date()
# start = datetime(end.year, end.month, 1).date()
def Home(start,end):
     
     col1,col2, status = st.columns(3)
     with col1:
          st.write('Income')
          inc = f"select sum(ammount) from expanses where date between  '{start}' and  '{end}' and e_type = 'Income'"
          cursor.execute(inc)
          income = cursor.fetchall() 
          st.success(income[0][0])
          # pass
     with col2:
          st.write('Expenses')
          inc = f"select sum(ammount) from expanses where date between  '{start}' and  '{end}' and e_type = 'Expense'"
          cursor.execute(inc)
          expenses = cursor.fetchall() 
          st.error(expenses[0][0])

def table_view(start,end):
     inc = f"select * from expanses where date between  '{start}' and  '{end}'"
     cursor.execute(inc)
     income = cursor.fetchall()
     column_name = [description[0] for description in cursor.description]
     df = pd.DataFrame(income, columns=column_name)
     return df

def pie_view(start,end):
     query = f"select catagories, sum(ammount) as amt from expanses where e_type = 'Expense' and date between '{start}' and  '{end}' group by catagories"
     cursor.execute(query)
     pie_data = cursor.fetchall()
     column_name = [description[0] for description in cursor.description]
     df = pd.DataFrame(pie_data, columns=column_name)
     fig = px.pie(df,values='amt',names='catagories', title="Expenses Pie chart")
     # pie_fig = fig.show()
     return fig
def pie_view_income(start,end):
     query = f"select catagories, sum(ammount) as amt from expanses where e_type = 'Income' and date between '{start}' and  '{end}' group by catagories"
     cursor.execute(query)
     pie_data = cursor.fetchall()
     column_name = [description[0] for description in cursor.description]
     df = pd.DataFrame(pie_data, columns=column_name)
     fig = px.pie(df,values='amt',names='catagories', title="Income Pie chart")
     return fig
def bar_view_income(start,end):
     query = f"select catagories, sum(ammount) as amt from expanses where e_type = 'Income' and date between '{start}' and  '{end}' group by catagories"
     cursor.execute(query)
     pie_data = cursor.fetchall()
     column_name = [description[0] for description in cursor.description]
     df = pd.DataFrame(pie_data, columns=column_name)
     fig = px.bar(df,x='catagories',y='amt', title="Income Pie chart")
     return fig
def bar_view_expenses(start,end):
     query = f"select catagories, sum(ammount) as amt from expanses where e_type = 'Expense' and date between '{start}' and  '{end}' group by catagories"
     cursor.execute(query)
     pie_data = cursor.fetchall()
     column_name = [description[0] for description in cursor.description]
     df = pd.DataFrame(pie_data, columns=column_name)
     fig = px.bar(df,x='catagories',y='amt', title="Expenses Pie chart")
     return fig
def bar_view_inc_exp(start,end):
     query = f"select e_type, sum(ammount) as amt from expanses where  date between '{start}' and  '{end}' group by e_type"
     cursor.execute(query)
     pie_data = cursor.fetchall()
     column_name = [description[0] for description in cursor.description]
     df = pd.DataFrame(pie_data, columns=column_name)
     fig = px.bar(df,x='e_type',y='amt',color='e_type' ,title="Expenses Pie chart")
     return fig

def graph_inc(start,end):
    query = f"SELECT date, SUM(ammount) as amt FROM expanses WHERE e_type = 'Income' AND date BETWEEN '{start}' AND '{end}' GROUP BY date order by date asc"
    cursor.execute(query)
    line_data = cursor.fetchall()
    column_name = [description[0] for description in cursor.description]
    df = pd.DataFrame(line_data, columns=column_name)
    fig = px.line(df, x='date', y='amt', title="Expenses Line Chart")
    return fig

def graph_exp(start,end):
     pass
